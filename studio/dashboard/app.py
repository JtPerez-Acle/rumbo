"""Observability dashboard for the 4-channel Spanish AI shorts studio.

Reads the studio's channels/, queue/ and output/ directories plus each
render task's stored parameters, and serves a single-page dashboard at
http://127.0.0.1:8765 with per-video publish tracking.

Run with the MoneyPrinterTurbo venv:
    MoneyPrinterTurbo/.venv/Scripts/python.exe studio/dashboard/app.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import tomllib
from pathlib import Path
from urllib.parse import quote

from fastapi import Cookie, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

STUDIO = Path(__file__).resolve().parents[1]
REPO = STUDIO.parent / "MoneyPrinterTurbo"
OUTPUT_DIR = STUDIO / "output"
PENDING_DIR = STUDIO / "queue" / "pending"
DONE_DIR = STUDIO / "queue" / "done"
FFPROBE = "ffprobe"
PLATFORMS = ["tiktok", "instagram", "youtube"]
DASHBOARD_TOKEN = os.environ.get("DASHBOARD_TOKEN", "")

sys.path.insert(0, str(STUDIO))

# True when running on Railway (any deployed environment). Used to decide the
# things that must be strict in production but stay convenient locally.
DEPLOYED = bool(os.environ.get("RAILWAY_ENVIRONMENT"))

# The interactive API docs enumerate every admin route and its body schema for
# anyone who asks. They were public in production (verified 2026-08-12). The
# allowlist is the real gate, but handing out the map is free reconnaissance.
app = FastAPI(
    title="Rumbo — Panel",
    docs_url=None if DEPLOYED else "/docs",
    redoc_url=None if DEPLOYED else "/redoc",
    openapi_url=None if DEPLOYED else "/openapi.json",
)


@app.on_event("startup")
def _ensure_schema() -> None:
    """Apply the additive schema on app startup, not just on container boot.

    entrypoint.py calls init_db() when the container starts, so production was
    always migrated — but running `uvicorn app:app` locally (the documented dev
    loop in docs/05) skipped it entirely. A new table therefore existed in db.py
    and in prod while every local test hit "relation does not exist". init_db is
    idempotent (CREATE TABLE / ADD COLUMN IF NOT EXISTS), so running it in both
    paths is free and keeps local and prod honest about the same schema.
    """
    from cloud import db                          # lazy, like the rest of app.py
    if not db.enabled():
        return
    try:
        db.init_db()
    except Exception as exc:                      # never block boot on the DB
        print(f"schema init skipped: {exc}", file=sys.stderr)
        return
    # Housekeeping (docs/06): expired sessions and spent magic links have no
    # reason to sit in the table. Cheap, idempotent, and boot is the natural
    # moment for it — there is no scheduler running in production.
    try:
        with db.connect() as conn:
            purged = db.purge_expired_auth(conn)
            conn.commit()
        if purged["sessions"] or purged["login_tokens"]:
            print(f"auth purge: {purged}", file=sys.stderr)
    except Exception as exc:
        print(f"auth purge skipped: {exc}", file=sys.stderr)


# Admin surface (token-gated). Everything else — the public site at /, the
# learner app at /aprende and its /api/learn/* routes — self-authenticates with a
# per-learner session or is public by design.
#
# The predicate lives in admin_paths.py so it can be audited without importing
# FastAPI: it is the allowlist the whole gate rests on, and a checker that cannot
# import it silently skips the only assertion that matters.
from admin_paths import is_admin_path as _is_admin_path  # noqa: E402
# The public site: where its built pages live, who is redirected past them, and
# robots/sitemap. Dependency-free for the same reason as admin_paths above — a
# check script must be able to assert it without importing FastAPI.
import public_site  # noqa: E402
# NOT `import site as public_site`: `site` is a stdlib module (it is what sets up
# sys.path at startup), so that import silently bound the standard library and
# every attribute lookup failed at import time.


def _https(request: Request) -> bool:
    """Railway terminates TLS at its proxy, so request.url.scheme says http."""
    proto = request.headers.get("x-forwarded-proto", "").split(",")[0].strip()
    return proto == "https" or request.url.scheme == "https"


# Headers applied to every response. The app renders Markdown compiled from
# learner submissions, so defence in depth around that sink is worth having.
#
# NO THIRD-PARTY SCRIPT ORIGIN, as of the Astro migration. marked, DOMPurify and
# mermaid are bundled from node_modules instead of fetched from a CDN with an
# SRI hash: the versions are pinned in package-lock.json, they cannot be swapped
# under us by a compromised CDN, and a phone on mobile data opens one fewer
# connection. `connect-src` lost the CDN with them.
#
# 'unsafe-inline' REMAINS, and it is worth being precise about why rather than
# repeating that it is temporary:
#   1. the operator dashboard (static/index.html) is still a single file with an
#      inline <script>. It is the next thing to migrate.
#   2. Astro emits a small inline bootstrap for each island.
# So CSP still does not stop injected inline script on its own, and DOMPurify at
# the render sink remains the actual XSS control. What this DOES buy: no
# plugins, no <base> hijack, no framing, no third-party script at all, and no
# mixed content.
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "img-src 'self' data: blob:; "
    "media-src 'self' blob:; "
    "connect-src 'self'; "
    "object-src 'none'; base-uri 'self'; form-action 'self'; "
    "frame-ancestors 'none'"
)


@app.middleware("http")
async def token_gate(request: Request, call_next):
    """Token gate for the admin dashboard only; learner routes pass through.

    Fails CLOSED in production. The gate used to be `if DASHBOARD_TOKEN and
    is_admin(path)`, so an unset or misspelled variable silently published the
    entire admin API — invite codes, learner PII, every submission — with no
    signal at all. Locally (no RAILWAY_ENVIRONMENT) an empty token still means
    "open", which is the documented dev loop in docs/05.
    """
    is_admin = _is_admin_path(request.url.path)
    if is_admin and not DASHBOARD_TOKEN and DEPLOYED:
        return JSONResponse(
            {"error": "admin surface disabled: DASHBOARD_TOKEN is not set"},
            status_code=503,
        )
    if DASHBOARD_TOKEN and is_admin:
        supplied = request.query_params.get("token") or request.cookies.get("studio_token")
        # Constant-time: a plain != leaks the token a character at a time to a
        # patient attacker with a stopwatch.
        if not supplied or not secrets.compare_digest(str(supplied), DASHBOARD_TOKEN):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        response = await call_next(request)
        response.set_cookie("studio_token", DASHBOARD_TOKEN, httponly=True,
                            samesite="lax", secure=_https(request),
                            max_age=90 * 86400)
        return _harden(response, request)
    return _harden(await call_next(request), request)


def _harden(response, request: Request):
    response.headers.setdefault("Content-Security-Policy", CSP)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy",
                                "geolocation=(), microphone=(), camera=()")
    if _https(request):
        response.headers.setdefault("Strict-Transport-Security",
                                    "max-age=31536000; includeSubDomains")
    return response


def load_channels() -> dict[str, dict]:
    channels = {}
    for path in sorted((STUDIO / "channels").glob("*.toml")):
        with open(path, "rb") as f:
            profile = tomllib.load(f)
        channels[profile["slug"]] = {
            "slug": profile["slug"],
            "name": profile["name"],
            "niche": profile.get("niche", ""),
            "audience": profile.get("audience", ""),
            "tone": profile.get("tone", ""),
            "voice": profile.get("voice", {}).get("voice_name", ""),
            "voice_rate": profile.get("voice", {}).get("voice_rate", 1.0),
            "color": profile.get("style", {}).get("stroke_color", "#888888"),
            "upload_post_username": profile.get("publish", {}).get("upload_post_username", ""),
            "platforms": profile.get("publish", {}).get("platforms", PLATFORMS),
        }
    return channels


def probe_duration(video: Path) -> float | None:
    try:
        out = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(video)],
            capture_output=True, text=True, timeout=15,
        )
        return round(float(out.stdout.strip()), 1)
    except (subprocess.SubprocessError, ValueError, OSError):
        return None


def read_sidecar(video: Path) -> dict:
    sidecar = video.with_suffix(".json")
    if sidecar.is_file():
        try:
            return json.loads(sidecar.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def write_sidecar(video: Path, meta: dict) -> None:
    video.with_suffix(".json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def task_details(task_id: str) -> dict:
    """Full render params + script as stored by the pipeline for one task."""
    script_json = REPO / "storage" / "tasks" / task_id / "script.json"
    if not script_json.is_file():
        return {}
    try:
        data = json.loads(script_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {
        "script": data.get("script", ""),
        "search_terms": data.get("search_terms", []),
        "params": data.get("params", {}),
    }


def collect_videos(channels: dict[str, dict]) -> list[dict]:
    videos = []
    if not OUTPUT_DIR.is_dir():
        return videos
    for channel_dir in sorted(OUTPUT_DIR.iterdir()):
        if not channel_dir.is_dir() or channel_dir.name not in channels:
            continue
        for mp4 in sorted(channel_dir.glob("*.mp4"), reverse=True):
            meta = read_sidecar(mp4)
            # Cache duration into the sidecar on first sight so ffprobe runs once.
            if "duration" not in meta:
                duration = probe_duration(mp4)
                if duration is not None:
                    meta["duration"] = duration
                    write_sidecar(mp4, meta)
            stat = mp4.stat()
            videos.append({
                "channel": channel_dir.name,
                "file": mp4.name,
                "url": f"/media/{channel_dir.name}/{mp4.name}",
                "size_mb": round(stat.st_size / 1_048_576, 1),
                "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
                "date": meta.get("date") or dt.date.fromtimestamp(stat.st_mtime).isoformat(),
                "duration": meta.get("duration"),
                "task_id": meta.get("task_id", ""),
                "subject": meta.get("subject", mp4.stem),
                "title": meta.get("title", mp4.stem),
                "description": meta.get("description", ""),
                "hashtags": meta.get("hashtags", []),
                "published": meta.get("published", {}),
                "approved": meta.get("approved"),
            })
    return videos


def collect_queue() -> dict:
    def read_dir(directory: Path) -> list[dict]:
        entries = []
        if directory.is_dir():
            for path in sorted(directory.glob("*.json")):
                try:
                    entry = json.loads(path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    continue
                entry["_file"] = path.name
                entries.append(entry)
        return entries
    return {"pending": read_dir(PENDING_DIR), "done": read_dir(DONE_DIR)}


@app.get("/api/state")
def get_state():
    channels = load_channels()
    videos = collect_videos(channels)
    queue = collect_queue()

    for ch in channels.values():
        ch_videos = [v for v in videos if v["channel"] == ch["slug"]]
        ch["video_count"] = len(ch_videos)
        ch["last_render"] = ch_videos[0]["modified"] if ch_videos else None
        ch["published_count"] = sum(1 for v in ch_videos if v["published"])

    published_total = sum(1 for v in videos if v["published"])
    approved_waiting = sum(1 for v in videos if v["approved"] and not v["published"])
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "channels": list(channels.values()),
        "videos": videos,
        "queue": queue,
        "summary": {
            "total_videos": len(videos),
            "pending": len(queue["pending"]),
            "published": published_total,
            "unpublished": len(videos) - published_total,
            "approved_waiting": approved_waiting,
            "storage_mb": round(sum(v["size_mb"] for v in videos), 1),
        },
    }


def _safe_media(channel: str, name: str) -> Path:
    """Resolve output/<channel>/<name>.mp4, refusing anything that escapes.

    `name` was traversal-checked but `channel` was not; both are path segments
    and both are attacker-shaped if the admin token ever leaks. Resolve and
    verify containment instead of pattern-matching for "..".
    """
    if ".." in name or ".." in channel or "/" in channel or "\\" in channel:
        raise HTTPException(404, "video not found")
    video = (OUTPUT_DIR / channel / name).resolve()
    if not str(video).startswith(str(OUTPUT_DIR.resolve())):
        raise HTTPException(404, "video not found")
    if not video.is_file() or video.suffix != ".mp4":
        raise HTTPException(404, "video not found")
    return video


@app.get("/api/videos/{channel}/{name}/details")
def get_video_details(channel: str, name: str):
    video = _safe_media(channel, name)
    meta = read_sidecar(video)
    return {**task_details(meta.get("task_id", "")), "meta": meta}


class PublishUpdate(BaseModel):
    platform: str
    value: bool


@app.post("/api/videos/{channel}/{name}/published")
def set_published(channel: str, name: str, update: PublishUpdate):
    if update.platform not in PLATFORMS:
        raise HTTPException(400, f"platform must be one of {PLATFORMS}")
    video = _safe_media(channel, name)
    meta = read_sidecar(video)
    published = meta.get("published", {})
    if update.value:
        published[update.platform] = dt.datetime.now().isoformat(timespec="seconds")
    else:
        published.pop(update.platform, None)
    meta["published"] = published
    write_sidecar(video, meta)
    return {"published": published}


class ApproveUpdate(BaseModel):
    value: bool


@app.post("/api/videos/{channel}/{name}/approve")
def set_approved(channel: str, name: str, update: ApproveUpdate):
    video = _safe_media(channel, name)
    meta = read_sidecar(video)
    if update.value:
        meta["approved"] = dt.datetime.now().isoformat(timespec="seconds")
    else:
        meta.pop("approved", None)
    write_sidecar(video, meta)
    return {"approved": meta.get("approved")}


_job_lock = threading.Lock()


def _run_job(target, *args) -> None:
    with _job_lock:
        target(*args)


@app.post("/api/jobs/{job}")
def trigger_job(job: str):
    """Manually fire the producer or a publish pass from the dashboard."""
    if _job_lock.locked():
        raise HTTPException(409, "a job is already running")
    if job == "produce":
        from cloud.producer import run_produce
        threading.Thread(target=_run_job, args=(run_produce,), daemon=True).start()
    elif job == "publish":
        from cloud.publisher import run_publish
        import datetime as _dt
        slot = min(["12:00", "19:00", "21:00"], key=lambda s: abs(
            int(s[:2]) * 60 - (_dt.datetime.now().hour * 60 + _dt.datetime.now().minute)))
        threading.Thread(target=_run_job, args=(run_publish, slot), daemon=True).start()
    else:
        raise HTTPException(400, "job must be 'produce' or 'publish'")
    return {"started": job}


@app.post("/api/upload-media")
async def upload_media(request: Request, rel_path: str = ""):
    """Admin-only (token-gated by middleware): push a rendered video to the volume
    at output/<rel_path>. Used to bulk-upload locally-rendered course videos.

    Streams the RAW body straight to the volume. The previous multipart version
    spooled through the container's ephemeral /tmp (starlette's form parser),
    which has ~20MB of headroom — every video over that failed with ENOSPC, a
    ceiling nobody hit until a course produced >20MB lessons. Multipart bodies
    are still accepted for back-compat, but the raw path is the reliable one.

    Writes to <dest>.part then os.replace: a failed upload can never truncate an
    existing good file again (tonight it zeroed 20 of them).
    """
    rel_path = rel_path.replace("\\", "/").lstrip("/")
    raw_mode = bool(rel_path)
    if not raw_mode:
        # Legacy multipart shape (rel_path in the form) — small files only.
        form = await request.form()
        rel_path = str(form.get("rel_path", "")).replace("\\", "/").lstrip("/")
        upload = form.get("file")
        if not rel_path or ".." in rel_path or upload is None:
            raise HTTPException(400, "rel_path and file required; no traversal")
    if ".." in rel_path:
        raise HTTPException(400, "no traversal")
    dest = (OUTPUT_DIR / rel_path).resolve()
    if not str(dest).startswith(str(OUTPUT_DIR.resolve())):
        raise HTTPException(400, "path escapes output dir")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    written = 0
    try:
        with open(tmp, "wb") as out:
            if raw_mode:
                async for chunk in request.stream():
                    out.write(chunk)
                    written += len(chunk)
            else:
                while True:
                    chunk = await upload.read(1 << 20)
                    if not chunk:
                        break
                    out.write(chunk)
                    written += len(chunk)
        if written == 0:
            raise HTTPException(400, "empty body")
        os.replace(tmp, dest)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
    return {"ok": True, "path": rel_path, "bytes": written}


@app.post("/api/delete-media")
def delete_media(rel_path: str = ""):
    """Admin-only (token-gated by middleware): remove one file from the volume.

    Exists for the shrink-and-replace flow: with the volume at 100%, an atomic
    replace can't even stage its .part file, so the old file must go first.
    Same traversal guards as upload; refuses directories.
    """
    rel_path = rel_path.replace("\\", "/").lstrip("/")
    if not rel_path or ".." in rel_path:
        raise HTTPException(400, "rel_path required; no traversal")
    dest = (OUTPUT_DIR / rel_path).resolve()
    if not str(dest).startswith(str(OUTPUT_DIR.resolve())):
        raise HTTPException(400, "path escapes output dir")
    if not dest.is_file():
        raise HTTPException(404, "no such file")
    size = dest.stat().st_size
    dest.unlink()
    return {"ok": True, "path": rel_path, "freed": size}


# ---- Learners: roster + access-link generator (the lockout escape hatch) ----

@app.get("/api/learners")
def list_learners():
    from cloud import db
    if not db.enabled():
        return {"learners": []}
    with db.connect() as conn:
        rows = conn.execute(
            "SELECT l.id, l.name, l.email, l.created_at, "
            "count(p.id) FILTER (WHERE p.completed_at IS NOT NULL) AS lessons_done, "
            "max(p.updated_at) AS last_activity "
            "FROM learners l LEFT JOIN progress p ON p.learner_id = l.id "
            "GROUP BY l.id ORDER BY last_activity DESC NULLS LAST, l.id"
        ).fetchall()
    return {"learners": rows}


@app.post("/api/learners/{learner_id}/login-link")
def learner_login_link(learner_id: int):
    """Mint a fresh magic link for a learner who lost their session — the
    operator sends it over WhatsApp/email until Resend automates this."""
    import secrets
    from cloud import db
    with db.connect() as conn:
        learner = conn.execute("SELECT id, email FROM learners WHERE id = %s",
                               (learner_id,)).fetchone()
        if not learner:
            raise HTTPException(404, "learner not found")
        token = secrets.token_urlsafe(24)
        db.create_login_token(conn, learner["id"], token, ttl_minutes=60 * 24)
        # Minting their link is the act of answering the request.
        db.resolve_access_request(conn, learner["email"])
        conn.commit()
    base = os.environ.get("PUBLIC_BASE_URL", "")
    return {"link": f"{base}/aprende/entrar?token={token}", "expires": "24h",
            "email": learner["email"]}


@app.get("/api/learners/{learner_id}/work")
def get_learner_work(learner_id: int):
    """Everything one learner has written, with the tutor's evaluation of each.
    At alpha scale this is the highest-signal data we have — the operator should
    be able to read 100% of it."""
    from cloud import db
    with db.connect() as conn:
        learner = conn.execute("SELECT * FROM learners WHERE id = %s", (learner_id,)).fetchone()
        if not learner:
            raise HTTPException(404, "learner not found")
        subs = db.learner_work(conn, learner_id)
        progress = db.learner_course_progress(conn, learner_id)
        docs = conn.execute(
            "SELECT pd.title, pd.share_token, pd.updated_at, c.title AS course_title "
            "FROM project_docs pd JOIN courses c ON c.id = pd.course_id "
            "WHERE pd.learner_id = %s ORDER BY pd.updated_at DESC", (learner_id,)).fetchall()
        requests = conn.execute(
            "SELECT topic, status, created_at FROM course_requests "
            "WHERE learner_id = %s ORDER BY id DESC", (learner_id,)).fetchall()
    out = []
    for s in subs:
        ev = s.get("evaluation") or {}
        out.append({
            "id": s["id"], "kind": s["kind"], "created_at": s["created_at"].isoformat(timespec="minutes"),
            "course_title": s.get("course_title") or "",
            "title": s.get("capstone_title") if s["kind"] == "capstone" else (s.get("node_title") or ""),
            "position": s.get("position"), "objectives": s.get("objectives") or "",
            "content": s["content"], "verdict": ev.get("verdict"),
            "rubric_version": ev.get("rubric_version"),
            "score": ev.get("score"), "final_score": ev.get("final_score", ev.get("score")),
            "dimensions": ev.get("dimensions"), "feedback": ev.get("feedback", ""),
            "misconception": ev.get("misconception"), "missing": ev.get("missing") or [],
            "improve": ev.get("improve", ""), "predicted": ev.get("predicted"),
            "defense_question": ev.get("defense_question"), "defense": ev.get("defense"),
            "defense_best": ev.get("defense_best"), "defense_attempts": ev.get("defense_attempts"),
            "flagged": s.get("flagged", False), "flag_note": s.get("flag_note") or "",
        })
    return {
        "learner": {"id": learner["id"], "name": learner["name"], "email": learner["email"],
                    "joined": learner["created_at"].date().isoformat()},
        "progress": progress, "submissions": out, "documents": docs, "requests": requests,
    }


class FlagBody(BaseModel):
    flagged: bool
    note: str = ""


@app.post("/api/submissions/{submission_id}/flag")
def flag_submission(submission_id: int, body: FlagBody):
    """Mark an evaluation the tutor got wrong. These flags are the labelled set
    we use to tune the evaluator prompts."""
    from cloud import db
    with db.connect() as conn:
        row = db.set_submission_flag(conn, submission_id, body.flagged, body.note.strip()[:500])
        conn.commit()
    if not row:
        raise HTTPException(404, "submission not found")
    return {"ok": True, **row}


@app.get("/api/access-requests")
def get_access_requests():
    """Learners locked out and waiting for a link.

    This queue exists because closing the account-takeover hole (2026-08-12)
    means a returning learner cannot let themselves back in until email delivery
    is configured. It should be EMPTY once `RESEND_API_KEY` is set — and if it
    starts filling up after that, email is broken and this is how you find out.
    """
    from cloud import db
    if not db.enabled():
        return {"requests": [], "email_configured": False}
    with db.connect() as conn:
        rows = [dict(r) for r in db.open_access_requests(conn)]
    for r in rows:
        r["created_at"] = r["created_at"].isoformat(timespec="minutes")
    # Fallback must name a domain that exists — aprende-ia.app never was
    # registered, so an unset EMAIL_FROM used to fail every send with an
    # unverified-domain error and show a healthy-looking sender here.
    sender = os.environ.get("EMAIL_FROM", "Rumbo <hola@ponrumbo.com>")
    return {"requests": rows,
            "email_configured": bool(os.environ.get("RESEND_API_KEY")),
            # The most dangerous state is not "email off" — it is email that
            # works for exactly ONE inbox. Resend's onboarding@resend.dev sender
            # needs no domain verification but will only deliver to the account
            # owner; every other recipient 403s. With a key set and this sender
            # configured, the dashboard would otherwise look healthy while the
            # entire cohort silently fails to receive anything.
            "sender": sender,
            "sender_is_test": "resend.dev" in sender}


@app.get("/api/demand")
def get_demand():
    """The demand ledger (docs/08's supply clock, finally instrumented).

    Answers the two questions the catalog cannot answer about itself: what do
    people ask to become that we cannot teach, and which of our own modules has
    any goal ever needed. The second one is the check on our worst habit —
    seven courses shipped in a single night while 80% of the library had never
    been routed to anyone.

    The build rule this exists to serve (docs/08): a gap earns a course when it
    RECURS, not when it appears. `build_candidates` applies that threshold so
    nobody has to eyeball the table and talk themselves into a course.
    """
    from cloud import db
    if not db.enabled():
        return {"analyses": 0, "gaps": [], "modules": [], "build_candidates": []}
    with db.connect() as conn:
        led = db.demand_ledger(conn)
    # Recurrence threshold. Deliberately low while volume is low, but never 1:
    # a single mention is one person's job posting, not a market.
    threshold = int(os.environ.get("GAP_BUILD_THRESHOLD", "3"))
    led["threshold"] = threshold
    led["build_candidates"] = [g for g in led["gaps"] if g["count"] >= threshold]
    return led


@app.get("/api/waitlist")
def get_waitlist():
    from cloud import db
    if not db.enabled():
        return {"waitlist": []}
    with db.connect() as conn:
        return {"waitlist": db.list_waitlist(conn)}


# ---- Invite codes: the access surface, managed from the dashboard ----

@app.get("/api/invites")
def get_invites(request: Request):
    """Every invite code with a ready-to-share link. Token-gated like the rest of
    the admin API — these codes ARE the access gate, so they never appear on a
    public surface."""
    from cloud import db
    if not db.enabled():
        return {"invites": [], "base": ""}
    with db.connect() as conn:
        rows = [dict(r) for r in db.list_invites(conn)]
    # Build links against the host actually being used, so a local dashboard
    # yields localhost links and production yields production ones. Trust
    # x-forwarded-proto: Railway terminates TLS at its proxy, so base_url reports
    # http and we would hand people an insecure-looking invite link to share.
    base = str(request.base_url).rstrip("/")
    proto = request.headers.get("x-forwarded-proto", "").split(",")[0].strip()
    if proto in ("http", "https"):
        base = re.sub(r"^https?://", f"{proto}://", base)
    for r in rows:
        r["link"] = f"{base}/login?invite={r['code']}"
        r["usable"] = bool(r["active"]) and r["uses"] < r["max_uses"]
    return {"invites": rows, "base": base}


class InviteBody(BaseModel):
    label: str = ""
    max_uses: int = 1


@app.post("/api/invites")
def post_invite(body: InviteBody):
    """Mint a code. Label is for the operator's own memory of who it went to."""
    import secrets as _secrets
    from cloud import db
    if not db.enabled():
        raise HTTPException(503, "sin base de datos")
    label = body.label.strip()[:120] or "sin etiqueta"
    max_uses = max(1, min(int(body.max_uses or 1), 500))
    code = _secrets.token_urlsafe(9)
    with db.connect() as conn:
        db.create_invite(conn, code, label, max_uses)
        conn.commit()
    return {"ok": True, "code": code, "label": label, "max_uses": max_uses}


@app.post("/api/invites/{code}/toggle")
def toggle_invite(code: str, active: bool = True):
    """Deactivate (or re-activate) a code without deleting it — the audit trail of
    who joined with which code stays intact."""
    from cloud import db
    if not db.enabled():
        raise HTTPException(503, "sin base de datos")
    with db.connect() as conn:
        db.set_invite_active(conn, code, active)
        conn.commit()
    return {"ok": True, "code": code, "active": active}


# ---- Course concierge: learner requests, triaged from the admin dashboard ----

@app.get("/api/requests")
def list_requests():
    from cloud import db
    if not db.enabled():
        return {"requests": []}
    with db.connect() as conn:
        return {"requests": db.all_course_requests(conn)}


class RequestUpdate(BaseModel):
    status: str
    course_slug: str = ""
    admin_note: str = ""


@app.post("/api/requests/{request_id}")
def update_request(request_id: int, update: RequestUpdate):
    from cloud import db
    if update.status not in db.REQUEST_STATUSES:
        raise HTTPException(400, f"status must be one of {db.REQUEST_STATUSES}")
    with db.connect() as conn:
        row = db.update_course_request(
            conn, request_id, update.status,
            update.course_slug.strip() or None, update.admin_note.strip() or None)
        conn.commit()
    if not row:
        raise HTTPException(404, "request not found")
    return {"ok": True, "request": row}


@app.get("/panel")
def panel():
    """The operator dashboard. Gated by _is_admin_path — check that first if you
    ever move this route, because the gate is an allowlist and a dashboard that
    is not on it ships public (docs/07)."""
    return FileResponse(Path(__file__).parent / "static" / "index.html")


# ---- Learner app (Rumbo) ----
from learn_routes import router as learn_router  # noqa: E402

app.include_router(learn_router)


@app.get("/aprende")
def aprende(request: Request, learner_session: str | None = Cookie(default=None)):
    """The learner app. Only for learners: it no longer contains a public half.

    Two query strings arrive here from links already in the world and must keep
    working — `?invite=CODE`, printed on every invite the operator has ever
    handed out, and `?error=` from a magic link that expired. Both used to open
    an in-app sign-in view; that view is a real page now, so they are forwarded
    with their query intact rather than broken.
    """
    from fastapi.responses import RedirectResponse
    if not _signed_in(learner_session):
        q = request.query_params
        invite, error = q.get("invite"), q.get("error")
        if invite:
            return RedirectResponse(f"/login?invite={quote(invite)}", status_code=302)
        if error:
            return RedirectResponse(f"/login?error={quote(error)}", status_code=302)
        # Nothing to sign in with: the public site is what they came for.
        return RedirectResponse("/", status_code=302)
    return FileResponse(public_site.page("/aprende"))


def _spa_shell(template: str, meta: dict | None = None):
    """Serve an SPA shell with server-injected <title>/OG tags.

    Only the three token share pages use this now. Link-preview crawlers on
    WhatsApp and LinkedIn never run JS, so the metadata has to be in the served
    document; the body still hydrates, which is fine for a page reached from a
    message rather than from a search result.

    It used to do four more things for the public surfaces — inject a
    prerendered body, a `__BOOT__` payload, a starting view, and `body.wide`.
    Those pages are static files now (site.py), and every one of those
    mechanisms existed only to make a hand-assembled document resemble the one
    hydration would build a moment later.
    """
    import html as _html
    import re as _re
    from fastapi.responses import HTMLResponse
    page = (Path(__file__).parent / "static" / template).read_text(encoding="utf-8")
    if meta:
        title = _html.escape(meta["title"], quote=True)
        desc = _html.escape(meta["description"], quote=True)
        page = page.replace("<title>", "<title data-og>", 1)
        page = _re.sub(r"<title data-og>.*?</title>", f"<title>{title}</title>",
                       page, count=1)
        tags = (f'<meta property="og:title" content="{title}">\n'
                f'<meta property="og:description" content="{desc}">\n'
                # website, not article: these are product surfaces, not posts.
                f'<meta property="og:type" content="website">\n'
                f'<meta name="description" content="{desc}">\n')
        page = page.replace("</head>", tags + "</head>", 1)
    return HTMLResponse(page)


def _share_page(template: str, meta: dict | None):
    """Back-compat name for the three token share pages."""
    return _spa_shell(template, meta)


# ---- The public site (docs/11) --------------------------------------------
# Static files, built by Astro in the Docker image and served straight off disk.
# These are NOT in _is_admin_path and must never be: they are the public face of
# the product.
#
# Each route is declared explicitly rather than mounted as a catch-all. A
# StaticFiles mount at "/" would shadow every API route it happened to match and
# would serve whatever appeared in the build directory; the admin gate is an
# allowlist, and an allowlist only works when the set of routes is known.

SITE_NAME = "Rumbo"


def _signed_in(learner_session: str | None) -> bool:
    """Whether this request carries a live learner session.

    Calls the endpoint function itself, so the answer can never disagree with
    what /api/learn/me would say. Any failure means "not signed in": showing a
    learner the public page is a small wrong, and refusing to serve the homepage
    because the database blinked is a large one.
    """
    if not learner_session:
        return False
    try:
        import learn_routes
        return bool(learn_routes.me(learner_session).get("authenticated"))
    except Exception as exc:
        print(f"session check failed, serving public page: {exc}", file=sys.stderr)
        return False


def _public(route: str, learner_session: str | None = None):
    """Serve a built public page, or send a signed-in learner into the app."""
    from fastapi.responses import RedirectResponse
    if learner_session and _signed_in(learner_session):
        target = public_site.SIGNED_IN_DESTINATION.get(route)
        if target:
            # 302, not 301: this depends on a cookie, and a browser that cached
            # it permanently would send a logged-OUT visitor to the app forever.
            return RedirectResponse(target, status_code=302)
    path = public_site.page(route)
    if not path.is_file():
        # The frontend build did not make it into the image. Say so loudly in
        # the log: a blank public site is the kind of failure that otherwise
        # gets discovered by a stranger.
        print(f"public page missing from the build: {path}", file=sys.stderr)
        raise HTTPException(503, "el sitio se está actualizando, vuelve en un minuto")
    return FileResponse(path)


@app.get("/")
def site_home(publica: str | None = None,
              learner_session: str | None = Cookie(default=None)):
    """The public site. This is what a stranger gets when they type the domain,
    and it used to be a 401 from a dashboard nobody but the operator can use.

    `?publica=1` shows it to a signed-in learner instead of redirecting them
    into the app. The operator is the only person with a permanent session and
    this is their own marketing page; without the escape hatch, looking at it
    means logging out of their own product. Perfil links here.
    """
    return _public("/", None if publica else learner_session)


@app.get("/cursos")
def public_cursos(learner_session: str | None = Cookie(default=None)):
    """The whole catalog at its own address. It used to exist only as a section
    below a full lesson on the landing, reachable by scrolling past all of it."""
    return _public("/cursos", learner_session)


@app.get("/curso/{slug}")
def public_curso(slug: str, learner_session: str | None = Cookie(default=None)):
    """A course temario at its own address. docs/02 calls the browsable temarios
    marketing content: 14 courses and 420 lesson objectives, all real, and until
    recently invisible to search because they lived behind a fragment."""
    from fastapi.responses import RedirectResponse
    if learner_session and _signed_in(learner_session):
        return RedirectResponse(f"/aprende#/explora/{slug}", status_code=302)
    route = f"/curso/{slug}"
    if not public_site.exists(route):
        # An unknown slug is not a broken build, it is a course that is not
        # ours. Sending it to the catalog beats a dead end.
        return RedirectResponse("/cursos", status_code=302)
    return FileResponse(public_site.page(route))


@app.get("/oferta")
def public_oferta(learner_session: str | None = Cookie(default=None)):
    """The job analyser. docs/08 calls this the acquisition asset and says it
    ships standalone — it could not be linked to before this route existed."""
    return _public("/oferta", learner_session)


@app.get("/lista")
def public_lista():
    """The waitlist. No redirect: someone already inside gains nothing from it
    and loses nothing either, and nobody arrives here holding a session."""
    return _public("/lista")


@app.get("/login")
def public_login(learner_session: str | None = Cookie(default=None)):
    """Sign-in. This was a 404 while the public header linked to it, so the
    primary way into the product from every public page was a dead end.

    It is a real URL rather than a fragment because it has to be linkable:
    "ve a ponrumbo.com/login" is a sentence someone says out loud."""
    return _public("/login", learner_session)


@app.get("/robots.txt", include_in_schema=False)
def robots():
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        public_site.robots_txt(os.environ.get("PUBLIC_BASE_URL", "")))


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap():
    from fastapi.responses import Response
    return Response(
        public_site.sitemap_xml(os.environ.get("PUBLIC_BASE_URL", ""),
                                public_site.course_slugs()),
        media_type="application/xml")


@app.get("/aprende/caso/{token}")
def aprende_caso(token: str):
    """Public share page for a learner's portfolio case study."""
    from cloud import db
    meta = None
    if db.enabled():
        try:
            with db.connect() as conn:
                row = db.case_study_by_token(conn, token)
            if row:
                meta = {"title": f"{row['title']} — {row['learner_name']}",
                        "description": f"Caso de estudio profesional de {row['learner_name']}, "
                                       f"elaborado con su trabajo real durante «{row['course_title']}»."}
        except Exception:
            meta = None
    return _share_page("caso.html", meta)


@app.get("/aprende/doc/{token}")
def aprende_doc(token: str):
    """Public page for a learner's project document (print-ready deliverable)."""
    from cloud import db
    meta = None
    if db.enabled():
        try:
            with db.connect() as conn:
                row = db.doc_by_token(conn, token)
            if row:
                desc = (f"Documento profesional elaborado por {row['learner_name']} "
                        f"durante el curso «{row['context']}»." if row["kind"] == "course"
                        else f"Documento profesional de {row['learner_name']}, hecho con su "
                             f"trabajo real y orientado al puesto «{row['context']}».")
                meta = {"title": f"{row['title']} — {row['learner_name']}",
                        "description": desc}
        except Exception:
            meta = None
    return _share_page("doc.html", meta)


@app.get("/aprende/ruta/{token}")
def aprende_ruta(token: str):
    """Public share page for a job-posting analysis (docs/08, docs/09).

    Shared at first contact rather than after weeks of coursework, and the
    remarkable part is the gap list — a platform publishing what it does NOT
    teach. The OG description therefore leads with coverage, not with the pitch.
    """
    from cloud import db
    meta = None
    if db.enabled():
        try:
            with db.connect() as conn:
                row = db.job_target_by_token(conn, token)
            if row:
                a = row["analysis"] or {}
                role = row["role_title"] or "este puesto"
                gaps = len(a.get("gaps") or [])
                falta = (f" y las {gaps} cosas que no cubrimos" if gaps > 1
                         else " y lo que no cubrimos" if gaps == 1 else "")
                meta = {"title": f"Ruta de estudio para {role} — Rumbo",
                        "description": f"Qué pide realmente el puesto, qué cubrimos "
                                       f"({a.get('coverage', 0)}%){falta}, y el documento "
                                       f"con el que llegarías a la entrevista."}
        except Exception:
            meta = None
    return _share_page("ruta.html", meta)


@app.get("/aprende/entrar")
def aprende_entrar(token: str):
    # Bounce through the API consumer, which sets the session cookie.
    from fastapi.responses import RedirectResponse
    return RedirectResponse(f"/api/learn/enter?token={token}", status_code=307)


if os.environ.get("ENABLE_SCHEDULER", "0") == "1":
    from cloud.scheduler import start_scheduler
    start_scheduler()


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=OUTPUT_DIR), name="media")

# The public site's CSS and island bundles. Every filename is content-hashed by
# the build, so these are immutable: a year of cache is safe and a deploy
# invalidates by changing the name. Mounted narrowly at /assets rather than
# serving the whole build directory, so nothing under it can shadow a route.
#
# Absent only when someone runs the server without building the frontend first
# (run_local.ps1 does it for you). The site 503s in that case and says why, so
# there is no need to fail the process here.
if public_site.DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=public_site.DIST / "assets"),
              name="web-assets")
else:
    print(f"frontend build missing at {public_site.DIST} — the public site will "
          f"503. Run: cd studio/web && npm ci && npm run build", file=sys.stderr)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")
