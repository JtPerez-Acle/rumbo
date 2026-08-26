"""Learner-facing API for the Aprende IA course app.

Separate front door from the admin dashboard: learners authenticate with a
magic link (dev mode returns the link directly when no email provider is set)
and get their own session cookie. Course videos stream through a session-checked
endpoint, never the public media mount.
"""
from __future__ import annotations

import os
import re
import secrets
import sys
import threading
import time
from collections import deque
from pathlib import Path

from fastapi import APIRouter, Cookie, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))
from cloud import db, writer  # noqa: E402

COURSE_SLUG = "curso-marketing-ia"
LESSONS_PER_DAY = int(os.environ.get("LESSONS_PER_DAY", "1"))
OUTPUT_DIR = STUDIO / "output"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# In-memory per-IP rate limiter for the login endpoint. Resets on redeploy —
# fine at this scale; move to Redis/DB if the service goes multi-instance.
_RATE: dict[str, deque] = {}
_RATE_MAX = int(os.environ.get("LOGIN_RATE_MAX", "8"))       # attempts
_RATE_WINDOW = int(os.environ.get("LOGIN_RATE_WINDOW", "300"))  # seconds


def _rate_ok(ip: str) -> bool:
    now = time.time()
    q = _RATE.setdefault(ip, deque())
    while q and now - q[0] > _RATE_WINDOW:
        q.popleft()
    if len(q) >= _RATE_MAX:
        return False
    q.append(now)
    return True


# The job analyser is public, unauthenticated, costs an LLM call and holds a
# worker for ~2 minutes. The login limiter (8 per 5 min) is far too generous for
# that, so it gets its own budget plus a hard cap on concurrent runs — without
# the cap a handful of tabs can starve the container for real learners.
_JOB_RATE: dict[str, deque] = {}
_JOB_RATE_MAX = int(os.environ.get("JOB_RATE_MAX", "3"))            # per IP
_JOB_RATE_WINDOW = int(os.environ.get("JOB_RATE_WINDOW", "3600"))   # seconds
_JOB_MAX_INFLIGHT = int(os.environ.get("JOB_MAX_INFLIGHT", "4"))
# A semaphore, not a counter: these handlers run in FastAPI's threadpool, so
# `_n += 1` is a read-modify-write race. Drifting downward would just loosen the
# cap, but drifting UPWARD would wedge the endpoint at 503 permanently.
# BoundedSemaphore also raises on over-release instead of silently drifting.
_JOB_SLOTS = threading.BoundedSemaphore(_JOB_MAX_INFLIGHT)


def _job_rate_ok(ip: str) -> bool:
    now = time.time()
    q = _JOB_RATE.setdefault(ip, deque())
    while q and now - q[0] > _JOB_RATE_WINDOW:
        q.popleft()
    if len(q) >= _JOB_RATE_MAX:
        return False
    q.append(now)
    return True


router = APIRouter(prefix="/api/learn")


def _current_learner(session: str | None) -> dict | None:
    if not db.enabled() or not session:
        return None
    with db.connect() as conn:
        return db.learner_for_session(conn, session)


def _require(session: str | None) -> dict:
    learner = _current_learner(session)
    if not learner:
        raise HTTPException(401, "no autenticado")
    return learner


class LoginBody(BaseModel):
    email: str
    name: str = ""
    invite: str = ""
    company: str = ""  # honeypot — real users never fill this hidden field


def _client_ip(request: Request) -> str:
    # Railway sets X-Forwarded-For; take the first hop.
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "unknown")


@router.post("/login")
def login(body: LoginBody, request: Request):
    """Invite-gated login. Requires a valid invite code (no email provider yet, so
    the code gates access). Rate-limited per IP, with a honeypot for bots. Issues a
    magic link — emailed if configured, otherwise returned so the invited user can
    proceed immediately."""
    if body.company.strip():  # honeypot tripped — silently no-op
        return {"sent": True}
    ip = _client_ip(request)
    if not _rate_ok(ip):
        raise HTTPException(429, "demasiados intentos, espera unos minutos")
    email = body.email.strip().lower()
    if not EMAIL_RE.match(email):
        raise HTTPException(400, "correo inválido")

    provider = os.environ.get("RESEND_API_KEY")
    with db.connect() as conn:
        existing = conn.execute("SELECT * FROM learners WHERE email = %s", (email,)).fetchone()
        # Returning users only skip the code when email delivery is configured
        # (inbox verifies identity). Without email, the code gates every login.
        if existing and provider:
            invite_row = None
        else:
            invite_row = db.valid_invite(conn, body.invite)
            if not invite_row:
                raise HTTPException(403, "Se requiere una invitación válida para entrar.")
        # An EXISTING account may only be entered by proving control of the
        # inbox. Without an email provider we cannot prove that, and returning
        # the magic link in the response body handed anyone who knew a learner's
        # address — plus any active invite code — a full session as that person.
        # Verified as a live account takeover during the 2026-08-12 audit.
        # A brand-new account has no such victim: the code IS the credential.
        if existing and not provider:
            # Queue them instead of leaving them at a dead end. Rate limiting
            # upstream (8 per 5 min per IP) keeps this from becoming a spam
            # surface, and the row is idempotent per email.
            db.record_access_request(conn, email, existing["id"],
                                     "sin proveedor de correo configurado")
            conn.commit()
            raise HTTPException(
                409,
                "Ya tienes una cuenta con ese correo. Por seguridad no podemos "
                "abrirte la sesión desde aquí todavía. Ya avisamos a tu instructor "
                "para que te mande tu enlace de acceso — normalmente es cuestión "
                "de horas.",
            )
        learner = db.get_or_create_learner(conn, email, body.name)
        if not existing:
            # New account: bind the code and consume one use.
            conn.execute("UPDATE learners SET invite_code = %s WHERE id = %s",
                         (body.invite.strip(), learner["id"]))
            if invite_row:
                db.consume_invite(conn, body.invite)
        token = secrets.token_urlsafe(24)
        db.create_login_token(conn, learner["id"], token)
        conn.commit()

    link = f"/aprende/entrar?token={token}"
    if provider:
        if _send_email(email, link):
            return {"sent": True}
        # Delivery failed. Never claim it worked: for a NEW account the code is
        # the credential and handing the link over directly is safe, but an
        # EXISTING account must still prove inbox control, so it goes to the
        # operator queue rather than to whoever asked.
        with db.connect() as conn:
            db.record_access_request(conn, email, learner["id"],
                                     "el envío de correo falló")
            conn.commit()
        if not existing:
            return {"sent": False, "dev_link": link,
                    "note": "No pudimos enviarte el correo, pero tu cuenta es nueva: entra con este enlace."}
        raise HTTPException(
            503,
            "No pudimos enviarte el correo en este momento. Ya avisamos a tu "
            "instructor para que te mande tu enlace de acceso.",
        )
    # Only ever reached for a NEW account (see the guard above).
    return {"sent": False, "dev_link": link}


def _send_email(email: str, link: str) -> bool:
    """Send the magic link. Returns whether it actually went out.

    This used to ignore the response completely, so a wrong key, an unverified
    sending domain or a Resend outage all looked identical to success: the
    learner was told "revisa tu correo" and waited for a message that was never
    accepted. That is the same silent-failure shape docs/06 flags for a dead
    OpenRouter key, and on a cohort it would strand people one at a time with
    nothing in any log to explain it.
    """
    import requests
    base = os.environ.get("PUBLIC_BASE_URL", "")
    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {os.environ['RESEND_API_KEY']}"},
            json={
                "from": os.environ.get("EMAIL_FROM", "Aprende IA <hola@aprende-ia.app>"),
                "to": [email],
                "subject": "Tu acceso a Aprende IA",
                "html": f'<p>Toca para entrar a tu clase de hoy:</p>'
                        f'<p><a href="{base}{link}">Entrar a Aprende IA</a></p>'
                        f'<p style="color:#888;font-size:12px">Si no fuiste tú, '
                        f'ignora este correo: el enlace caduca y es de un solo uso.</p>',
                "text": f"Entra a tu clase de hoy: {base}{link}\n\n"
                        f"El enlace caduca y es de un solo uso.",
            },
            timeout=20,
        )
        if r.status_code >= 300:
            # Body carries Resend's reason (unverified domain, bad key, …) and
            # is what turns "no llegó el correo" into a five-second diagnosis.
            print(f"resend send failed [{r.status_code}] to {email}: {r.text[:300]}",
                  file=sys.stderr)
            return False
        return True
    except Exception as exc:
        print(f"resend send error to {email}: {exc}", file=sys.stderr)
        return False


def _is_https(request: Request) -> bool:
    """True when the browser is really talking HTTPS. Railway terminates TLS at
    its proxy, so request.url.scheme reports http — trust x-forwarded-proto.
    Local dev over plain http gets secure=False so the cookie still works."""
    proto = request.headers.get("x-forwarded-proto", "").split(",")[0].strip()
    return proto == "https" or request.url.scheme == "https"


@router.get("/enter")
def enter(token: str, request: Request):
    """Consume a magic-link token, mint a session, set the cookie, redirect in."""
    with db.connect() as conn:
        learner_id = db.consume_login_token(conn, token)
        if not learner_id:
            conn.commit()
            return RedirectResponse("/aprende?error=enlace_invalido", status_code=303)
        session = secrets.token_urlsafe(32)
        db.create_session(conn, learner_id, session)
        # They are back in, so they are no longer waiting. Self-clearing beats a
        # queue the operator has to remember to tidy.
        row = conn.execute("SELECT email FROM learners WHERE id = %s",
                           (learner_id,)).fetchone()
        if row:
            db.resolve_access_request(conn, row["email"])
        conn.commit()
    resp = RedirectResponse("/aprende", status_code=303)
    resp.set_cookie("learner_session", session, httponly=True, samesite="lax",
                    secure=_is_https(request), max_age=db.SESSION_DAYS * 86400)
    return resp


@router.post("/logout")
def logout(learner_session: str | None = Cookie(default=None)):
    """Revoke the session server-side, then clear the cookie.

    Dropping the cookie alone left the token valid in the database — logout that
    only logs out the browser is not logout."""
    if learner_session and db.enabled():
        try:
            with db.connect() as conn:
                db.delete_session(conn, learner_session)
                conn.commit()
        except Exception:            # never fail a logout on a DB hiccup
            pass
    resp = JSONResponse({"ok": True})
    resp.delete_cookie("learner_session")
    return resp


def _node_with_course(conn, node_id: int):
    node = conn.execute("SELECT * FROM syllabus_nodes WHERE id = %s", (node_id,)).fetchone()
    if not node:
        return None, None, []
    course = conn.execute("SELECT * FROM courses WHERE id = %s", (node["course_id"],)).fetchone()
    nodes = db.course_nodes(conn, node["course_id"])
    return node, course, nodes


def _accessible_ids(nodes: list[dict], completed: set[int],
                    route_modules: set[int] | None = None,
                    exempt_modules: set[int] | None = None) -> set[int]:
    """Completed lessons + the first uncompleted (progress gate) are open.

    Route-aware widening (docs/09): when the learner's active route selects
    specific modules of this course, the first uncompleted lesson WITHIN the
    selected modules is also open — a mid-course entry point. Skipping is safe
    because the matcher's module sets are prereq-closed server-side. The rule
    only ever WIDENS access: a learner without a route, or on a course outside
    their route, gets exactly the original behavior.

    Exemption-aware widening (docs/10): a module the learner has skipped — said
    they already know it, or credited it by passing its reto — should not be
    where the course tries to start them, so the first uncompleted lesson in a
    NON-exempt module is opened too. This also only ever adds: every lesson of a
    skipped module stays exactly as reachable as it was, because removing
    content from someone who wants it is the failure mode, and hiding is not
    locking.
    """
    acc = set(completed)
    for n in nodes:  # ordered by position
        if n["id"] not in completed:
            acc.add(n["id"])
            break
    if route_modules:
        for n in nodes:
            if n["module_no"] in route_modules and n["id"] not in completed:
                acc.add(n["id"])
                break
    if exempt_modules:
        pool = [n for n in nodes if n["module_no"] not in exempt_modules]
        if route_modules:
            pool = [n for n in pool if n["module_no"] in route_modules]
        nxt = next((n for n in pool if n["id"] not in completed), None)
        if nxt:
            acc.add(nxt["id"])
    return acc


def _accessible_for(conn, learner_id: int, course: dict, nodes: list[dict],
                    completed: set[int]) -> set[int]:
    """THE place access is computed. One function, one rule.

    Every widening source (route module sets, CV exemptions) has to be applied
    at every gate — lesson, video, submit, reteach, complete, temario — and this
    codebase's recurring failure shape is a new rule added to some call sites and
    not others (docs/07: "security by allowlist"). Both sources here only ever
    ADD, so a missed call site costs a learner a shortcut rather than opening a
    hole; consolidating still beats relying on that.
    """
    return _accessible_ids(
        nodes, completed,
        _route_modules_for(conn, learner_id, course["slug"]),
        db.exempt_modules_for(conn, learner_id, course["id"]),
    )


def _route_modules_for(conn, learner_id: int, course_slug: str) -> set[int] | None:
    """The module set the learner's active route selects in this course, or None
    when there is no active target / the course is not on the route. v1 rows
    (no "modules" list) expand to the prefix they always meant."""
    target = db.active_job_target(conn, learner_id)
    if not target:
        return None
    for r in ((target["analysis"] or {}).get("ruta") or []):
        if r.get("course_slug") == course_slug:
            mods = r.get("modules")
            if isinstance(mods, list) and mods:
                return {int(x) for x in mods}
            return set(range(1, int(r.get("through_module", 1)) + 1))
    return None


def _learner_context(learner: dict) -> str:
    """The declared transversal project as evaluator context. Empty string when
    nothing is declared, which keeps the evaluation prompt byte-identical to the
    pre-context behavior."""
    parts = []
    if learner.get("project_name"):
        parts.append(f"Proyecto: {learner['project_name']}.")
    if learner.get("project_desc"):
        parts.append(learner["project_desc"])
    if learner.get("goal"):
        parts.append(f"Su objetivo: {learner['goal']}.")
    return " ".join(parts)


@router.get("/me")
def me(learner_session: str | None = Cookie(default=None)):
    learner = _current_learner(learner_session)
    if not learner:
        return {"authenticated": False}
    return {"authenticated": True, "name": learner["name"], "email": learner["email"],
            "project_name": learner.get("project_name") or "",
            "project_desc": learner.get("project_desc") or "",
            "goal": learner.get("goal") or ""}


class ProfileBody(BaseModel):
    project_name: str = ""
    project_desc: str = ""
    goal: str = ""


@router.post("/profile")
def update_profile(body: ProfileBody, learner_session: str | None = Cookie(default=None)):
    """Declare (or update) the transversal project: the one real business, brand,
    organization or team every exercise builds on. Learner-level, not per-course
    (docs/09) — it is what lets work compile across courses into one goal
    document, and what the evaluator judges Aplicación against."""
    learner = _require(learner_session)
    with db.connect() as conn:
        db.set_learner_profile(conn, learner["id"], body.project_name.strip(),
                               body.project_desc.strip(), body.goal.strip())
        conn.commit()
    return {"ok": True}


@router.get("/today")
def today(learner_session: str | None = Cookie(default=None)):
    """The Hoy tab: continue-card, due reviews (the SM-2 surface), open defensas,
    streak. The zero-decision daily entry point."""
    learner = _require(learner_session)
    with db.connect() as conn:
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        # Continue: the course they touched most recently → its next open lesson.
        cont = None
        latest = conn.execute(
            "SELECT n.course_id FROM progress p JOIN syllabus_nodes n ON n.id = p.node_id "
            "WHERE p.learner_id = %s ORDER BY p.updated_at DESC LIMIT 1",
            (learner["id"],)).fetchone()
        if latest:
            c = conn.execute("SELECT * FROM courses WHERE id = %s",
                             (latest["course_id"],)).fetchone()
            nodes = db.course_nodes(conn, c["id"])
            # docs/10: never point the continue-card at a module they skipped.
            skipped = db.exempt_modules_for(conn, learner["id"], c["id"])
            nxt = next((n for n in nodes
                        if n["id"] not in completed and n["module_no"] not in skipped), None)
            if nxt:
                cont = {"course_slug": c["slug"], "course_title": c["title"],
                        "lesson_id": nxt["id"], "lesson_title": nxt["title"],
                        "position": nxt["position"], "total": len(nodes),
                        "has_video": bool(nxt["video_file"])}
            else:
                cont = {"course_slug": c["slug"], "course_title": c["title"],
                        "finished": True, "total": len(nodes)}
        # Due reviews: completed lessons whose SM-2 clock has struck.
        reviews = conn.execute(
            "SELECT p.node_id AS lesson_id, n.title AS lesson_title, n.position, "
            "c.title AS course_title, c.slug AS course_slug "
            "FROM progress p JOIN syllabus_nodes n ON n.id = p.node_id "
            "JOIN courses c ON c.id = n.course_id "
            "WHERE p.learner_id = %s AND p.completed_at IS NOT NULL "
            "AND p.next_review_at IS NOT NULL AND p.next_review_at <= now() "
            "ORDER BY p.next_review_at LIMIT 5",
            (learner["id"],)).fetchall()
        # Open defensas: evaluated work whose ownership question is unanswered.
        # Pending conversations, with the exact place to answer them: a lesson
        # step (explica/ejercicio) or a capstone. Unreachable pending items were
        # a real dead end — every one of these must be one tap away.
        defenses = []
        for s in db.latest_submissions(conn, learner["id"]):
            ev = s.get("evaluation") or {}
            # Conversations belong to work products — an explain has no
            # decisions to own, so it never generates one.
            if s["kind"] == "explain":
                continue
            if not ev.get("defense_question") or ev.get("defense"):
                continue
            if s["node_id"]:
                node = conn.execute(
                    "SELECT title FROM syllabus_nodes WHERE id = %s", (s["node_id"],)).fetchone()
                if not node:
                    continue
                defenses.append({
                    "kind": s["kind"], "lesson_id": s["node_id"],
                    "lesson_title": node["title"],
                    "step": "explica" if s["kind"] == "explain" else "ejercicio",
                    "question": ev["defense_question"]})
            elif s["capstone_id"]:
                cap = db.get_capstone(conn, s["capstone_id"])
                if not cap:
                    continue
                defenses.append({
                    "kind": "capstone", "capstone_id": cap["id"],
                    "lesson_title": f"Reto: {cap['title']}",
                    "question": ev["defense_question"]})
        streak = db.streak_days(conn, learner["id"])
        done_today = db.completions_today(conn, learner["id"])
    return {"continue": cont, "reviews": reviews, "defenses": defenses[:3],
            "streak": streak, "done_today": done_today,
            "name": learner["name"] or learner["email"].split("@")[0]}


# ---- Public layer: the platform's face for strangers. Catalog and temarios are
# marketing content; lessons, videos and evaluations stay behind the invite gate.

@router.get("/public/catalog")
def public_catalog():
    out = []
    with db.connect() as conn:
        rows = conn.execute("SELECT * FROM courses ORDER BY id").fetchall()
        for c in rows:
            nodes = db.course_nodes(conn, c["id"])
            if not nodes:
                continue
            rendered = sum(1 for n in nodes if n["video_file"])
            tpl = writer.PROJECT_TEMPLATES.get(c["slug"], writer.PROJECT_TEMPLATES["default"])
            out.append({"slug": c["slug"], "title": c["title"],
                        "description": c.get("description") or "",
                        "category": c.get("category") or "",
                        "total": len(nodes),
                        "modules": len({n["module_no"] for n in nodes}),
                        "doc_type": tpl["doc_type"],
                        "available": rendered > 0})
    return {"courses": out}


@router.get("/public/course/{slug}")
def public_course(slug: str):
    with db.connect() as conn:
        c = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
        if not c:
            raise HTTPException(404, "curso no encontrado")
        nodes = db.course_nodes(conn, c["id"])
    modules: dict[int, dict] = {}
    for n in nodes:
        m = modules.setdefault(n["module_no"], {
            "module_no": n["module_no"], "module_title": n["module_title"],
            "module_description": n.get("module_description") or "", "lessons": []})
        m["lessons"].append({"position": n["position"], "title": n["title"],
                             "objectives": n.get("objectives") or ""})
    tpl = writer.PROJECT_TEMPLATES.get(slug, writer.PROJECT_TEMPLATES["default"])
    return {"slug": c["slug"], "title": c["title"],
            "description": c.get("description") or "", "doc_type": tpl["doc_type"],
            "total": len(nodes), "modules": [modules[k] for k in sorted(modules)]}


class WaitlistBody(BaseModel):
    name: str = ""
    email: str
    motivo: str = ""
    company: str = ""  # honeypot


@router.post("/waitlist")
def join_waitlist(body: WaitlistBody, request: Request):
    if body.company.strip():
        return {"ok": True}
    ip = _client_ip(request)
    if not _rate_ok(ip):
        raise HTTPException(429, "demasiados intentos, espera unos minutos")
    email = body.email.strip().lower()
    if not EMAIL_RE.match(email):
        raise HTTPException(400, "correo inválido")
    with db.connect() as conn:
        db.add_waitlist(conn, body.name.strip()[:120], email, body.motivo.strip()[:500])
        conn.commit()
    return {"ok": True}


class JobPostingBody(BaseModel):
    posting: str = ""
    goal: str = ""     # docs/09 item 4: "quiero ser X" without a posting
    company: str = ""  # honeypot


def _route_progress(conn, learner_id: int, analysis: dict) -> dict:
    """How much of a CANDIDATE route the learner has already completed.

    The point of showing this before they commit: progress is keyed per lesson,
    not per goal, so changing goals carries work forward instead of restarting.
    That is true in the data and invisible without this."""
    prog = db.progress_map(conn, learner_id)
    completed = {nid for nid, p in prog.items() if p["completed_at"]}
    per, done_all, total_all = [], 0, 0
    for r in (analysis.get("ruta") or []):
        c = conn.execute("SELECT * FROM courses WHERE slug = %s",
                         (r["course_slug"],)).fetchone()
        if not c:
            continue
        mods = r.get("modules")
        selected = ({int(x) for x in mods} if isinstance(mods, list) and mods
                    else set(range(1, int(r.get("through_module", 1)) + 1)))
        nodes = [n for n in db.course_nodes(conn, c["id"]) if n["module_no"] in selected]
        done = sum(1 for n in nodes if n["id"] in completed)
        done_all += done
        total_all += len(nodes)
        per.append({"course_slug": r["course_slug"], "done": done, "lessons": len(nodes)})
    return {"done": done_all, "total": total_all, "per_course": per}


@router.post("/public/job-analysis")
def job_analysis(body: JobPostingBody, request: Request,
                 learner_session: str | None = Cookie(default=None)):
    """Match a job posting OR a stated goal against the catalog (docs/08, 09).

    Deliberately PUBLIC: a stranger pastes a posting — or just names the role
    they want — sees the route, the honest gaps and the document they would walk
    in with, and only then meets the invite wall — at peak intent. Putting this
    behind auth would defeat it (the concierge is behind auth and has zero rows).
    """
    if body.company.strip():          # honeypot tripped — silently no-op
        raise HTTPException(400, "no pudimos leer esa oferta")
    goal = body.goal.strip()
    posting = body.posting.strip()
    if goal:
        if not 5 <= len(goal) <= 140:
            raise HTTPException(400, "dinos el puesto o la habilidad en una frase "
                                     "(5 a 140 caracteres)")
        posting, mode = goal, "goal"
    else:
        mode = "posting"
        if len(posting) < 200:
            raise HTTPException(400, "pega la oferta completa: necesitamos los "
                                     "requisitos para armarte una ruta real")
        if len(posting) > 12000:
            raise HTTPException(400, "esa oferta es muy larga, pega solo la parte de "
                                     "funciones y requisitos")
    # An existing learner exploring a new offer is a legitimate, attributable
    # action — it should not spend the anonymous per-IP budget (3/h), which is
    # there to stop strangers burning LLM calls. Authed callers get the
    # per-learner evaluation budget instead.
    learner = _current_learner(learner_session)
    if learner:
        if not _eval_rate_ok(learner["id"]):
            raise HTTPException(429, "alcanzaste el límite por ahora, intenta más tarde")
    elif not _job_rate_ok(_client_ip(request)):
        raise HTTPException(429, "ya analizamos varias ofertas desde aquí. "
                                 "Espera un rato y vuelve a intentar.")
    if not _JOB_SLOTS.acquire(blocking=False):
        raise HTTPException(503, "estamos analizando varias ofertas ahora mismo. "
                                 "Intenta de nuevo en un par de minutos.")
    try:
        with db.connect() as conn:
            catalog = db.job_catalog(conn)
        if not catalog:
            raise HTTPException(503, "catálogo no disponible")
        try:
            analysis = writer.analyze_job_posting(posting, catalog, mode=mode)
        except Exception as exc:
            # writer._chat already retried. A raw 500 here would show a stranger
            # a blank failure on the acquisition surface, so say something true
            # and recoverable instead.
            print(f"job analysis failed: {exc}", file=sys.stderr)
            raise HTTPException(503, "no pudimos terminar el análisis. Vuelve a "
                                     "intentarlo en unos minutos.")
        token = secrets.token_urlsafe(12)
        progress = None
        with db.connect() as conn:
            # Authed: attribute the target immediately but leave it INACTIVE — a
            # candidate the learner still has to accept. Anonymous rows stay
            # unattributed until claimed at first login.
            db.save_job_target(conn, posting, analysis, token,
                               learner_id=learner["id"] if learner else None)
            if learner:
                progress = _route_progress(conn, learner["id"], analysis)
            conn.commit()
    finally:
        _JOB_SLOTS.release()
    return {"ok": True, "token": token, "analysis": analysis,
            "authenticated": bool(learner), "progress": progress}


# ---- The live lesson: the landing IS the product running (docs/11) ---------
# A stranger cannot try this product — access is invite-gated — and its value
# (verified work, not video) is invisible from outside. Every competitor claims
# an AI tutor; nobody can tell them apart by reading. So the public surface
# teaches one real lesson and evaluates one real answer BEFORE asking for
# anything, and the invite wall arrives after value was delivered rather than
# before.
#
# ONE lesson, fixed server-side. The node id is never taken from the caller:
# this codebase already shipped a bug where a write granted a read (docs/07),
# and the mirror of it is an unauthenticated read that accepts an id. A demo
# endpoint parameterised by node_id would publish all 420 gated videos.
DEMO_NODE_ID = int(os.environ.get("DEMO_NODE_ID", "1"))
# Strangers get a much tighter budget than the job analyser (3/h): the analyser
# is worth an expensive call because a posting is high intent, while this fires
# on curiosity.
_DEMO_MAX = int(os.environ.get("DEMO_RATE_MAX", "4"))
_DEMO_WINDOW = int(os.environ.get("DEMO_RATE_WINDOW", "3600"))
_DEMO_RATE: dict[str, deque] = {}


def _demo_rate_ok(ip: str) -> bool:
    now = time.time()
    q = _DEMO_RATE.setdefault(ip, deque())
    while q and now - q[0] > _DEMO_WINDOW:
        q.popleft()
    if len(q) >= _DEMO_MAX:
        return False
    q.append(now)
    return True


def _demo_node(conn):
    node = conn.execute("SELECT * FROM syllabus_nodes WHERE id = %s",
                        (DEMO_NODE_ID,)).fetchone()
    if not node:
        return None, None
    course = conn.execute("SELECT * FROM courses WHERE id = %s",
                          (node["course_id"],)).fetchone()
    return node, course


@router.get("/public/demo")
def public_demo():
    """The one lesson a stranger can actually take, whole: video, key points,
    written guide and the question. No auth, no id, nothing to enumerate."""
    with db.connect() as conn:
        node, course = _demo_node(conn)
        if not node:
            raise HTTPException(503, "demo no disponible")
        caps = db.course_capstones(conn, course["id"])
    quiz = node.get("quiz") or {}
    ex = (quiz.get("exercise") or {}) if isinstance(quiz, dict) else {}
    tpl = writer.PROJECT_TEMPLATES.get(course["slug"], writer.PROJECT_TEMPLATES["default"])
    reto = next((c for c in caps if c["module_no"] == node["module_no"]), None)
    return {
        "course_slug": course["slug"], "course_title": course["title"],
        "module_no": node["module_no"],
        "module_title": node.get("module_title") or "",
        "title": node["title"],
        "objectives": node.get("objectives") or "",
        "key_points": node.get("key_points") or [],
        "written": node.get("written") or "",
        "transcript": node.get("transcript") or "",
        "explain_prompt": node.get("explain_prompt") or "",
        "has_video": bool(node["video_file"]),
        # What comes AFTER the free lesson, shown as real content rather than a
        # claim: the exercise this lesson ends in, the module's reto, and the
        # document the course compiles into.
        "exercise": {"instruction": ex.get("instruction", ""),
                     "deliverable": ex.get("deliverable", "")} if ex else None,
        "reto": {"title": reto["title"], "scenario": reto["scenario"]} if reto else None,
        "doc_type": tpl["doc_type"],
    }


@router.get("/public/demo-video")
def public_demo_video():
    """The demo lesson's video, and only ever that one. Deliberately takes no
    parameter: see DEMO_NODE_ID."""
    with db.connect() as conn:
        node, _ = _demo_node(conn)
    if not node or not node["video_file"]:
        raise HTTPException(404, "video no disponible")
    path = OUTPUT_DIR / node["video_file"]
    if not path.is_file():
        raise HTTPException(404, "archivo no encontrado")
    return FileResponse(path, media_type="video/mp4")


class DemoExplainBody(BaseModel):
    content: str = ""
    company: str = ""      # honeypot, same as every other public text intake


@router.post("/public/demo-explain")
def public_demo_explain(body: DemoExplainBody, request: Request):
    """Evaluate a stranger's answer to the demo lesson's question.

    This is the whole argument of the surface: they get a real verdict from the
    real evaluator, on their own words, before meeting any wall. It returns a
    verdict and never a score, exactly like the logged-in explain step — putting
    a number on a comprehension check is a category error this product already
    made once (docs/02).
    """
    if body.company.strip():                 # honeypot tripped — silently no-op
        raise HTTPException(400, "no pudimos leer tu respuesta")
    content = body.content.strip()
    if not 40 <= len(content) <= 4000:
        raise HTTPException(400, "escribe tu respuesta con tus palabras: "
                                 "entre 40 y 4000 caracteres")
    ip = _client_ip(request)
    if not _demo_rate_ok(ip):
        raise HTTPException(429, "ya evaluamos varias respuestas desde aquí. "
                                 "Pide tu invitación y seguimos adentro.")
    if not _JOB_SLOTS.acquire(blocking=False):
        raise HTTPException(503, "estamos evaluando varias respuestas ahora mismo. "
                                 "Intenta en un par de minutos.")
    try:
        with db.connect() as conn:
            node, _ = _demo_node(conn)
        if not node:
            raise HTTPException(503, "demo no disponible")
        try:
            evaluation = writer.evaluate_explanation(node, content)
        except Exception as exc:
            print(f"demo explain failed: {exc}", file=sys.stderr)
            raise HTTPException(503, "no pudimos evaluar tu respuesta ahora. "
                                     "Intenta de nuevo en un momento.")
        # Kept because it is the only record of what a stranger writes when
        # asked to explain something. At 16 real submissions total, that is the
        # evidence this project is short of, and it costs one row.
        try:
            with db.connect() as conn:
                db.record_demo_attempt(conn, node["id"], content, evaluation)
                conn.commit()
        except Exception as exc:                    # never fail the learner on telemetry
            print(f"demo attempt not stored: {exc}", file=sys.stderr)
    finally:
        _JOB_SLOTS.release()
    return {"ok": True, "evaluation": {
        "verdict": evaluation.get("verdict"),
        "feedback": evaluation.get("feedback", ""),
        "misconception": evaluation.get("misconception"),
        "missing": evaluation.get("missing") or [],
    }}


@router.get("/public/ruta/{token}")
def public_route(token: str):
    """The analysis as a public, shareable artifact (docs/09).

    The portfolio document is the platform's viral loop but needs 3+ submissions
    to exist — weeks of engagement. This one exists two minutes after a stranger
    pastes a posting, and the part worth sharing is the honest gap list. No auth:
    the unguessable token is the capability, same as /doc and /caso.
    """
    with db.connect() as conn:
        row = db.job_target_by_token(conn, token)
    if not row:
        raise HTTPException(404, "ruta no encontrada")
    return {"role_title": row["role_title"], "company": row["company"],
            "learner_name": row["learner_name"] or "",
            "created_at": row["created_at"].isoformat(),
            "analysis": row["analysis"]}


class ClaimBody(BaseModel):
    token: str


@router.post("/job-target/claim")
def claim_route(body: ClaimBody, learner_session: str | None = Cookie(default=None)):
    """Make a target this learner's ACTIVE goal. Serves two jobs:

    1. Claiming an analysis made before signing up (token parked in the browser,
       so the claim has to come from the client once a session exists).
    2. SWITCHING goals — activating a candidate they just analysed, or going back
       to one they set aside. `db.claim_job_target` deactivates their others and
       permits re-activating a target they already own.

    Non-destructive either way: completed lessons are keyed per lesson so they
    carry into the new route, and the previous goal keeps its own document.
    Idempotent, and it refuses a token owned by someone else.
    """
    learner = _require(learner_session)
    with db.connect() as conn:
        row = db.claim_job_target(conn, body.token.strip(), learner["id"])
        conn.commit()
    if not row:
        raise HTTPException(404, "esa ruta no existe o es de otra persona")
    return {"ok": True, "role_title": row["role_title"]}


@router.get("/job-target")
def my_job_target(learner_session: str | None = Cookie(default=None)):
    """The learner's active goal with live progress against its route.

    Returns the route two ways. `route` is the per-course summary. `steps` is the
    SPINE: one entry per selected module, in order, each labelled by its outcome
    contract ("sabrás hacer X") with the course demoted to provenance. That is
    what makes this a path through knowledge instead of a list of courses to buy.

    Progress measures the ROUTE, never whole courses — the route is the promise.
    next_lesson is the first uncompleted lesson inside it, always reachable by
    the widened access rule."""
    learner = _require(learner_session)
    with db.connect() as conn:
        target = db.active_job_target(conn, learner["id"])
        if not target:
            return {"exists": False}
        analysis = target["analysis"] or {}
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        # docs/10: modules the learner skipped. They stay IN the route (the route
        # is the honest answer to "what does this job need"), but they are marked,
        # they are not where we start anyone, and they come out of what is left
        # to do — which is the number the learner actually feels.
        exempt_state = _exemption_view(conn, learner["id"])
        route, steps, next_lesson = [], [], None
        exempt_lessons = exempt_modules = 0
        for r in (analysis.get("ruta") or []):
            c = conn.execute("SELECT * FROM courses WHERE slug = %s",
                             (r["course_slug"],)).fetchone()
            if not c:
                continue
            nodes = db.course_nodes(conn, c["id"])
            # v2 routes carry a module SET; v1 rows expand to the prefix they meant.
            mods = r.get("modules")
            selected = ({int(x) for x in mods} if isinstance(mods, list) and mods
                        else set(range(1, int(r.get("through_module", 1)) + 1)))
            in_route = [n for n in nodes if n["module_no"] in selected]
            skipped = {m for m in selected
                       if f"{r['course_slug']}:{m}" in exempt_state}
            done = sum(1 for n in in_route if n["id"] in completed)
            for m in skipped:
                exempt_modules += 1
                exempt_lessons += sum(1 for n in in_route
                                      if n["module_no"] == m and n["id"] not in completed)
            if next_lesson is None:
                # First uncompleted lesson INSIDE the route's module set and NOT
                # in a skipped module — by the widened access rule it is always
                # reachable.
                pending = next((n for n in in_route
                                if n["id"] not in completed
                                and n["module_no"] not in skipped), None)
                if pending:
                    next_lesson = {"node_id": pending["id"], "title": pending["title"],
                                   "course_title": c["title"]}
            route.append({"course_slug": r["course_slug"], "course_title": c["title"],
                          "modules": sorted(selected),
                          "through_module": r["through_module"], "phase": r.get("phase", "nucleo"),
                          "lessons": len(in_route), "done": done, "why": r.get("why", "")})
            # THE SPINE: one step per selected module, in route order, labelled by
            # what the learner will be able to DO. The course is provenance, not
            # the unit — docs/09 settled that the module is the unit, and every
            # surface still rendered courses, which is why the product read as a
            # shop rather than a path through knowledge.
            for m in sorted(selected):
                in_mod = [n for n in in_route if n["module_no"] == m]
                if not in_mod:
                    continue
                m_done = sum(1 for n in in_mod if n["id"] in completed)
                pending = next((n for n in in_mod if n["id"] not in completed), None)
                ex = exempt_state.get(f"{r['course_slug']}:{m}")
                steps.append({
                    "course_slug": r["course_slug"], "course_title": c["title"],
                    "module_no": m, "module_title": in_mod[0].get("module_title") or "",
                    "outcome": in_mod[0].get("module_description") or "",
                    "phase": r.get("phase", "nucleo"),
                    "lessons": len(in_mod), "done": m_done,
                    "next_lesson_id": pending["id"] if pending else None,
                    # None | "declarado" | "acreditado" (docs/10). The step stays
                    # visible either way: the job still needs it, and the lessons
                    # are still open if they want them.
                    "exempt": ex["status"] if ex else None,
                    "exempt_score": ex["score"] if ex else None,
                })
        gd = db.get_goal_doc(conn, learner["id"], target["id"])
    total = sum(r["lessons"] for r in route)
    done = sum(r["done"] for r in route)
    return {"exists": True, "target_id": target["id"],
            # What is actually left after the skips — the number that turns an
            # honest-but-unstartable 84-lesson route into one someone opens.
            "exempt_lessons": exempt_lessons, "exempt_modules": exempt_modules,
            "remaining": max(0, total - done - exempt_lessons),
            "role_title": target["role_title"], "company": target["company"],
            "coverage": analysis.get("coverage", 0), "gaps": analysis.get("gaps") or [],
            "doc_type": analysis.get("doc_type", ""), "route": route,
            # `steps` is the route as a PATH; `route` stays for the per-course
            # summary and older consumers.
            "steps": steps,
            "done": done, "total": total, "next_lesson": next_lesson,
            "share_url": f"/aprende/ruta/{target['share_token']}" if target["share_token"] else "",
            "goal_doc": {"exists": bool(gd), "title": gd["title"] if gd else "",
                         "share_url": f"/aprende/doc/{gd['share_token']}" if gd else ""}}


@router.get("/job-targets")
def my_job_targets(learner_session: str | None = Cookie(default=None)):
    """The learner's goals, for switching between them. Non-destructive: changing
    goals keeps every completed lesson (progress is per lesson) and every goal
    document (keyed per target)."""
    learner = _require(learner_session)
    with db.connect() as conn:
        rows = db.learner_job_targets(conn, learner["id"])
        out = []
        for r in rows:
            a = r["analysis"] or {}
            p = _route_progress(conn, learner["id"], a)
            out.append({
                "token": r["share_token"], "role_title": r["role_title"],
                "company": r["company"], "active": r["active"],
                "coverage": a.get("coverage", 0), "doc_type": a.get("doc_type", ""),
                "has_doc": r["has_doc"], "created_at": r["created_at"].date().isoformat(),
                "done": p["done"], "total": p["total"],
            })
    return {"targets": out}


# ---- CV intake (docs/10): the CV proposes, the reto disposes ---------------
# A CV is a CLAIM about what someone already knows, and this product exists
# because claims are not trusted — work is. So none of these endpoints can widen
# access. `POST /cv` returns PROPOSALS; accepting one shortens the route and
# opens that module's reto early; only PASSING the reto (a novel case,
# deliberately not covered in the lessons) credits the module. That is the whole
# security argument: an injected CV reaches "declarado" and stops there.

class CvBody(BaseModel):
    cv: str = ""
    company: str = ""     # honeypot, same as the other public-ish text intakes


def _exemption_view(conn, learner_id: int) -> dict:
    """Every exemption keyed "<slug>:<module_no>", for merging into any surface."""
    out = {}
    for e in db.learner_exemptions(conn, learner_id):
        out[f"{e['course_slug']}:{e['module_no']}"] = {
            "status": e["status"], "source": e["source"], "score": e["score"],
            "course_title": e["course_title"], "module_no": e["module_no"],
            "course_slug": e["course_slug"], "claim": e["claim"] or "",
        }
    return out


def _cv_payload(conn, learner_id: int, profile: dict | None) -> dict:
    """The CV reading plus what the learner has since DONE with each proposal.

    The analysis is a snapshot of what the model read; the exemptions are the
    live state. Keeping them separate means re-reading the CV never silently
    revokes a credited module.
    """
    if not profile:
        return {"exists": False, "pass_score": writer.EXEMPTION_PASS_SCORE,
                "exemptions": list(_exemption_view(conn, learner_id).values())}
    analysis = profile["analysis"] or {}
    state = _exemption_view(conn, learner_id)
    claims = []
    for c in (analysis.get("claims") or []):
        st = state.get(f"{c['course_slug']}:{c['module_no']}")
        claims.append({**c, "state": st["status"] if st else "pendiente",
                       "exempt_score": st["score"] if st else None})
    return {
        "exists": True,
        # The bar the reto has to clear, straight from the server: the screen
        # must never promise a threshold the backend does not enforce.
        "pass_score": writer.EXEMPTION_PASS_SCORE,
        "created_at": profile["created_at"].date().isoformat(),
        "headline": analysis.get("headline", ""),
        "years_experience": analysis.get("years_experience", 0),
        "claims": claims,
        "fuera_del_catalogo": analysis.get("fuera_del_catalogo") or [],
        "proposed_modules": analysis.get("proposed_modules", 0),
        "proposed_lessons": analysis.get("proposed_lessons", 0),
        "exemptions": list(state.values()),
    }


@router.post("/cv")
def submit_cv(body: CvBody, learner_session: str | None = Cookie(default=None)):
    """Read a CV and propose module exemptions. Requires a session on purpose.

    Unlike the job analyser — which is deliberately public because it is the
    acquisition surface — a CV is personal data with no acquisition value to us
    and every reason to stay attached to one account. Contact details are
    stripped BEFORE the text is stored or sent to the model.
    """
    if body.company.strip():                  # honeypot tripped — silently no-op
        raise HTTPException(400, "no pudimos leer ese CV")
    learner = _require(learner_session)
    cv = writer.strip_contacts(body.cv.strip())
    if len(cv) < 200:
        raise HTTPException(400, "pega tu CV completo: con la experiencia y lo que "
                                 "hiciste en cada puesto, no solo los títulos")
    if len(cv) > 20000:
        raise HTTPException(400, "ese CV es muy largo, pega la parte de experiencia")
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite por ahora, intenta más tarde")
    if not _JOB_SLOTS.acquire(blocking=False):
        raise HTTPException(503, "estamos analizando varios CV ahora mismo. "
                                 "Intenta de nuevo en un par de minutos.")
    try:
        with db.connect() as conn:
            catalog = db.job_catalog(conn)
        if not catalog:
            raise HTTPException(503, "catálogo no disponible")
        try:
            analysis = writer.analyze_cv(cv, catalog)
        except Exception as exc:
            print(f"cv analysis failed: {exc}", file=sys.stderr)
            raise HTTPException(503, "no pudimos terminar de leer tu CV. Vuelve a "
                                     "intentarlo en unos minutos.")
        with db.connect() as conn:
            profile = db.save_cv_profile(conn, learner["id"], cv, analysis)
            conn.commit()
            payload = _cv_payload(conn, learner["id"], profile)
    finally:
        _JOB_SLOTS.release()
    return {"ok": True, **payload}


@router.get("/cv")
def my_cv(learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        return _cv_payload(conn, learner["id"],
                           db.active_cv_profile(conn, learner["id"]))


@router.delete("/cv")
def forget_cv(learner_session: str | None = Cookie(default=None)):
    """Forget the CV and every skip it proposed.

    CREDITED modules survive deliberately: those were earned by passing a reto,
    and nothing a learner earned may ever go down (docs/07). Deleting the CV
    removes what we were told, never what they proved.
    """
    learner = _require(learner_session)
    with db.connect() as conn:
        dropped = db.clear_declared_exemptions(conn, learner["id"])
        removed = db.delete_cv_profiles(conn, learner["id"])
        conn.commit()
    return {"ok": True, "profiles_deleted": removed, "exemptions_cleared": dropped}


class ExemptionBody(BaseModel):
    course_slug: str
    module_no: int
    action: str = "skip"          # skip | teach
    claim: str = ""


@router.post("/exemption")
def set_exemption(body: ExemptionBody, learner_session: str | None = Cookie(default=None)):
    """Accept a proposed skip, or undo one ("enséñamelo igual").

    `skip` is cosmetic by design: it shortens the route, opens that module's reto
    early, and changes NO access — every lesson stays exactly as reachable as it
    was. `teach` can only undo a DECLARED skip; a credited module is a passed
    reto, not a preference.
    """
    learner = _require(learner_session)
    if body.action not in ("skip", "teach"):
        raise HTTPException(400, "acción no válida")
    with db.connect() as conn:
        course = conn.execute("SELECT * FROM courses WHERE slug = %s",
                              (body.course_slug,)).fetchone()
        if not course:
            raise HTTPException(404, "curso no encontrado")
        modules = {n["module_no"] for n in db.course_nodes(conn, course["id"])}
        if body.module_no not in modules:
            raise HTTPException(404, "módulo no encontrado")
        if body.action == "skip":
            db.set_module_exemption(conn, learner["id"], course["id"],
                                    body.module_no, claim=body.claim[:400], source="cv")
            conn.commit()
            return {"ok": True, "status": "declarado",
                    "exemptions": list(_exemption_view(conn, learner["id"]).values())}
        cleared = db.clear_module_exemption(conn, learner["id"], course["id"],
                                            body.module_no)
        conn.commit()
        if not cleared:
            # Either there was nothing to clear, or it is credited — say which,
            # because "nothing happened" reads as a bug.
            state = _exemption_view(conn, learner["id"]).get(
                f"{body.course_slug}:{body.module_no}")
            if state and state["status"] == "acreditado":
                raise HTTPException(
                    409, "Ese módulo lo acreditaste con su reto. Puedes ver sus "
                         "lecciones cuando quieras: no lo quitamos de tu historial.")
        return {"ok": True, "status": "pendiente",
                "exemptions": list(_exemption_view(conn, learner["id"]).values())}


@router.get("/goal-doc")
def goal_doc_status(learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        target = db.active_job_target(conn, learner["id"])
        if not target:
            return {"exists": False, "eligible": False, "submissions": 0}
        subs = _route_submissions(conn, learner["id"], target["analysis"] or {})
        gd = db.get_goal_doc(conn, learner["id"], target["id"])
    # Same floor as the per-course document (docs/02): below it there is not
    # enough real work to compile from, and the compiler fills the vacuum by
    # inventing. Observed at n=1: a market-research section with a fabricated
    # user search query, from a submission that only said "falta oferta local".
    return {"exists": bool(gd), "eligible": len(subs) >= MIN_CASE_STUDY_SUBMISSIONS,
            "needed": MIN_CASE_STUDY_SUBMISSIONS, "submissions": len(subs),
            "title": gd["title"] if gd else "",
            "content_md": gd["content_md"] if gd else "",
            "share_url": f"/aprende/doc/{gd['share_token']}" if gd else ""}


@router.post("/goal-doc")
def generate_goal_doc(learner_session: str | None = Cookie(default=None)):
    """Compile the goal document: the learner's best work across every course in
    the route, organized by the posting's own competencies (docs/09). Regenerable
    as they progress; the share link stays stable.

    Gated on MIN_CASE_STUDY_SUBMISSIONS pieces of REAL WORK — real meaning it
    cleared MIN_PORTFOLIO_SCORE, which excludes non-attempts (a pasted starter
    prompt, an off-task line), NOT weak work. A bad-but-genuine attempt is
    exactly the raw material this is for.

    "Honest thinness beats a locked door" was the original reasoning, and one
    submission is not thinness — it is absence, which the compiler fills by
    inventing (it once produced a whole skills inventory from a starter prompt).
    The same floor guards the course document and the case study."""
    learner = _require(learner_session)
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite de evaluaciones por ahora, intenta más tarde")
    with db.connect() as conn:
        target = db.active_job_target(conn, learner["id"])
        if not target:
            raise HTTPException(400, "primero analiza la oferta del trabajo que quieres "
                                     "(tu objetivo) — el documento se arma hacia ese puesto")
        analysis = target["analysis"] or {}
        if not analysis.get("ruta"):
            raise HTTPException(400, "tu objetivo no tiene ruta de estudio, no hay qué compilar")
        subs = _route_submissions(conn, learner["id"], analysis)
        if len(subs) < MIN_CASE_STUDY_SUBMISSIONS:
            raise HTTPException(
                400, f"tienes {len(subs)} de {MIN_CASE_STUDY_SUBMISSIONS} trabajos "
                     f"necesarios para armar el documento. Envía ejercicios de los "
                     f"cursos de tu ruta, con tu proyecto real: de entregas vacías no "
                     f"sale un documento honesto, y este documento lo vas a mostrar.")
        existing = db.get_goal_doc(conn, learner["id"], target["id"])
    name = learner["name"] or learner["email"].split("@")[0]
    try:
        result = writer.compose_goal_doc(analysis, name, _learner_context(learner), subs)
    except RuntimeError:
        raise HTTPException(503, "no pudimos compilar tu documento ahora, intenta en un momento")
    token = existing["share_token"] if existing else secrets.token_urlsafe(12)
    with db.connect() as conn:
        gd = db.upsert_goal_doc(conn, learner["id"], target["id"],
                                result["title"], result["content_md"], token)
        conn.commit()
    return {"ok": True, "title": gd["title"], "content_md": gd["content_md"],
            "share_url": f"/aprende/doc/{gd['share_token']}"}


@router.get("/courses")
def courses(learner_session: str | None = Cookie(default=None)):
    """Catalog of all courses with this learner's progress. Courses without
    rendered videos yet show as 'coming soon'."""
    learner = _require(learner_session)
    out = []
    with db.connect() as conn:
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        rows = conn.execute("SELECT * FROM courses ORDER BY id").fetchall()
        for c in rows:
            nodes = db.course_nodes(conn, c["id"])
            if not nodes:
                continue
            rendered = sum(1 for n in nodes if n["video_file"])
            done = sum(1 for n in nodes if n["id"] in completed)
            tpl = writer.PROJECT_TEMPLATES.get(c["slug"], writer.PROJECT_TEMPLATES["default"])
            out.append({
                "slug": c["slug"], "title": c["title"],
                "description": c.get("description") or "",
                "category": c.get("category") or "",
                "total": len(nodes), "done": done,
                "modules": len({n["module_no"] for n in nodes}),
                "doc_type": tpl["doc_type"],
                "available": rendered > 0,
                "rendered": rendered,
            })
    return {"courses": out, "streak": _streak(learner["id"])}


def _streak(learner_id: int) -> int:
    with db.connect() as conn:
        return db.streak_days(conn, learner_id)


@router.get("/course/{slug}")
def course_outline(slug: str, learner_session: str | None = Cookie(default=None)):
    """Full temario: modules → lessons with per-lesson status for navigation."""
    learner = _require(learner_session)
    with db.connect() as conn:
        c = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
        if not c:
            raise HTTPException(404, "curso no encontrado")
        nodes = db.course_nodes(conn, c["id"])
        prog = db.progress_map(conn, learner["id"])
        capstones = _capstone_states(conn, c["id"], learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        accessible = _accessible_for(conn, learner["id"], c, nodes, completed)
        exempt = {e["module_no"]: e for e in db.learner_exemptions(conn, learner["id"])
                  if e["course_slug"] == slug}
    modules: dict[int, dict] = {}
    for n in nodes:
        has_video = bool(n["video_file"])
        if n["id"] in completed:
            status = "done"
        elif n["id"] in accessible and has_video:
            status = "current"
        elif n["id"] in accessible and not has_video:
            status = "coming"      # it's your next lesson but not rendered yet
        else:
            status = "locked"
        ex = exempt.get(n["module_no"])
        m = modules.setdefault(n["module_no"], {"module_no": n["module_no"],
                                                "module_title": n["module_title"],
                                                "module_description": n.get("module_description") or "",
                                                "lessons": [],
                                                "capstone": capstones.get(n["module_no"]),
                                                # docs/10: skipped, not locked —
                                                # every lesson below is still open.
                                                "exempt": ex["status"] if ex else None,
                                                "exempt_score": ex["score"] if ex else None})
        m["lessons"].append({
            "id": n["id"], "position": n["position"], "title": n["title"],
            "objectives": n.get("objectives") or "",
            "status": status, "score": (prog.get(n["id"]) or {}).get("quiz_score"),
        })
    return {
        "slug": c["slug"], "title": c["title"],
        "description": c.get("description") or "",
        "total": len(nodes), "done": len(completed),
        "modules": [modules[k] for k in sorted(modules)],
    }


@router.get("/profile")
def profile(learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        streak = db.streak_days(conn, learner["id"])
        rows = conn.execute("SELECT * FROM courses ORDER BY id").fetchall()
        per = []
        total_done = 0
        for c in rows:
            nodes = db.course_nodes(conn, c["id"])
            if not nodes:
                continue
            done = sum(1 for n in nodes if n["id"] in completed)
            total_done += done
            if done:
                per.append({"title": c["title"], "done": done, "total": len(nodes)})
    return {
        "name": learner["name"] or learner["email"].split("@")[0],
        "email": learner["email"], "streak": streak,
        "lessons_done": total_done, "courses": per,
        "project_name": learner.get("project_name") or "",
        "project_desc": learner.get("project_desc") or "",
        "goal": learner.get("goal") or "",
    }


@router.get("/lesson/{node_id}")
def lesson(node_id: int, learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        node, course, nodes = _node_with_course(conn, node_id)
        if not node:
            raise HTTPException(404, "lección no encontrada")
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        accessible = _accessible_for(conn, learner["id"], course, nodes, completed)
        if node["id"] not in accessible:
            raise HTTPException(403, "esta lección aún no está disponible")
        # The learner's own history belongs in the lesson, not hidden in Perfil:
        # a revisit greets them with their last work and its evaluation.
        prev_explain, n_explain = _previous_submission(
            conn, learner["id"], "explain", node_id=node["id"])
        prev_exercise, n_exercise = _previous_submission(
            conn, learner["id"], "exercise", node_id=node["id"])
    # Adjacent lessons that are accessible (for prev/next navigation).
    ordered = sorted(nodes, key=lambda n: n["position"])
    idx = next(i for i, n in enumerate(ordered) if n["id"] == node["id"])
    prev_id = next((ordered[j]["id"] for j in range(idx - 1, -1, -1)
                    if ordered[j]["id"] in accessible), None) if idx > 0 else None
    next_id = ordered[idx + 1]["id"] if idx + 1 < len(ordered) and ordered[idx + 1]["id"] in accessible else None
    quiz = node["quiz"] or {}
    return {
        "id": node["id"], "course_slug": course["slug"],
        "position": node["position"], "total": len(nodes),
        "module_no": node["module_no"], "module_title": node["module_title"],
        "title": node["title"], "objectives": node["objectives"],
        "video_url": f"/api/learn/video/{node['id']}" if node["video_file"] else "",
        "transcript": node.get("transcript") or "",
        "explain_prompt": node.get("explain_prompt") or "",
        "key_points": node.get("key_points") or [],
        "written": node.get("written") or "",
        "diagrams": node.get("diagrams") or [],
        "quiz": quiz.get("questions", []),
        "exercise": quiz.get("exercise", {}),
        "is_review": node["id"] in completed,
        "prev_id": prev_id, "next_id": next_id,
        "last_explain": ({"content": prev_explain["content"],
                          "evaluation": _evaluation_out(prev_explain, attempt=n_explain)}
                         if prev_explain else None),
        "last_exercise": ({"content": prev_exercise["content"],
                           "evaluation": _evaluation_out(prev_exercise, attempt=n_exercise)}
                          if prev_exercise else None),
    }


@router.get("/video/{node_id}")
def video(node_id: int, learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        node, course, nodes = _node_with_course(conn, node_id)
        if node:
            # Same lock model as the lesson endpoint: completed + the next one.
            prog = db.progress_map(conn, learner["id"])
            completed = {nid for nid, p in prog.items() if p["completed_at"]}
            if node["id"] not in _accessible_for(
                    conn, learner["id"], course, nodes, completed):
                raise HTTPException(403, "esta lección aún no está disponible")
    if not node or not node["video_file"]:
        raise HTTPException(404, "video no disponible")
    path = OUTPUT_DIR / node["video_file"]
    if not path.is_file():
        raise HTTPException(404, "archivo no encontrado")
    return FileResponse(path, media_type="video/mp4")


# Per-learner limiter for LLM-evaluated submissions (cost control; in-memory,
# same trade-off as the login limiter).
_EVAL_RATE: dict[int, deque] = {}
# Retries are now encouraged (work + conversation, both unlimited), so the cap
# has to sit well above an enthusiastic session. Each evaluation costs a
# fraction of a cent; this is an abuse backstop, not a budget.
_EVAL_MAX = int(os.environ.get("EVAL_RATE_MAX", "60"))          # evaluations
_EVAL_WINDOW = int(os.environ.get("EVAL_RATE_WINDOW", "3600"))  # seconds


def _eval_rate_ok(learner_id: int) -> bool:
    now = time.time()
    q = _EVAL_RATE.setdefault(learner_id, deque())
    while q and now - q[0] > _EVAL_WINDOW:
        q.popleft()
    if len(q) >= _EVAL_MAX:
        return False
    q.append(now)
    return True


def _final_score(ev: dict) -> int | None:
    return ev.get("final_score", ev.get("score"))


def _evaluation_out(sub: dict, attempt: int | None = None) -> dict:
    ev = sub.get("evaluation") or {}
    return {
        "id": sub["id"], "kind": sub["kind"],
        # Comprehension checks carry a verdict; work products carry a score.
        "verdict": ev.get("verdict"),
        "score": ev.get("score"), "passed": ev.get("passed"),
        "final_score": _final_score(ev),
        "dimensions": ev.get("dimensions"),
        "feedback": ev.get("feedback", ""),
        "misconception": ev.get("misconception"),
        "missing": ev.get("missing") or [],
        "improve": ev.get("improve", ""),
        "defense_question": ev.get("defense_question"),
        "defense": ev.get("defense"),
        "defense_best": ev.get("defense_best"),
        "defense_attempts": ev.get("defense_attempts"),
        "predicted": ev.get("predicted"),
        "attempt": attempt,
        "created_at": sub["created_at"].date().isoformat(),
    }


def _previous_submission(conn, learner_id: int, kind: str,
                         node_id: int | None = None,
                         capstone_id: int | None = None) -> tuple[dict | None, int]:
    """Newest prior attempt for this exact work item, plus how many attempts exist."""
    if capstone_id:
        rows = conn.execute(
            "SELECT * FROM submissions WHERE learner_id = %s AND kind = %s "
            "AND capstone_id = %s ORDER BY id DESC", (learner_id, kind, capstone_id),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM submissions WHERE learner_id = %s AND kind = %s "
            "AND node_id = %s ORDER BY id DESC", (learner_id, kind, node_id),
        ).fetchall()
    return (rows[0] if rows else None), len(rows)


def _prompt_snapshot(kind: str, node: dict | None = None,
                     capstone: dict | None = None) -> dict:
    """Exactly what the learner was answering, frozen at submit time.

    Lesson content is compiled output and WILL be regenerated. Without this the
    node_id is a dangling pointer: improve an exercise and every past submission
    silently becomes an answer to a question nobody asked, evaluated against a
    prompt that no longer exists — and the portfolio document, which is the
    credibility artifact this product sells, quotes it under the new heading.
    """
    if kind == "capstone" and capstone:
        return {"kind": "capstone", "title": capstone.get("title", ""),
                "scenario": capstone.get("scenario", ""),
                "deliverable": capstone.get("deliverable", ""),
                "rubric": capstone.get("rubric") or []}
    if not node:
        return {"kind": kind}
    base = {"kind": kind, "lesson_title": node.get("title", ""),
            "objectives": node.get("objectives", "")}
    if kind == "explain":
        base["question"] = node.get("explain_prompt") or ""
    else:
        ex = (node.get("quiz") or {}).get("exercise", {}) or {}
        base["instruction"] = ex.get("instruction", "")
        base["starting_point"] = ex.get("starting_point", "")
    return base


class SubmitBody(BaseModel):
    node_id: int
    kind: str          # explain | exercise
    content: str
    predicted: int | None = None   # optional self-assessment (calibration)


@router.post("/submit")
def submit(body: SubmitBody, learner_session: str | None = Cookie(default=None)):
    """Evaluate a learner's own words (explain-back) or exercise artifact against
    the lesson, via the LLM. Feedback teaches; nothing here gates progression."""
    learner = _require(learner_session)
    if body.kind not in ("explain", "exercise"):
        raise HTTPException(400, "kind inválido")
    content = body.content.strip()
    if not 20 <= len(content) <= 5000:
        raise HTTPException(400, "escribe entre 20 y 5000 caracteres")
    with db.connect() as conn:
        node, course, nodes = _node_with_course(conn, body.node_id)
        if not node:
            raise HTTPException(404, "lección no encontrada")
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        if node["id"] not in _accessible_for(
                conn, learner["id"], course, nodes, completed):
            raise HTTPException(403, "esta lección aún no está disponible")
        previous, prior_attempts = _previous_submission(
            conn, learner["id"], body.kind, node_id=node["id"])
        # Identical text must never produce a different number. Re-grading an
        # unchanged submission is where the worst regression in the product came
        # from: the same 1687 characters scored 79, then 50, then 30, because the
        # evaluator punishes a retry that ignored its feedback. That is a fair
        # instinct and a terrible measurement — the score stops describing the
        # work. So an unchanged resubmission is not an evaluation at all: return
        # what it already earned, say plainly that nothing changed, and spend no
        # LLM call or rate-limit budget on it.
        if previous and (previous["content"] or "").strip() == content:
            out = _evaluation_out(previous, attempt=prior_attempts)
            out["unchanged"] = True
            out["best_score"] = db.best_score_for(
                conn, learner["id"], body.kind, node_id=node["id"])
            return {"ok": True, "unchanged": True, "evaluation": out}
        best_before = db.best_score_for(
            conn, learner["id"], body.kind, node_id=node["id"])
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite de evaluaciones por ahora, intenta más tarde")
    try:
        if body.kind == "explain":
            evaluation = writer.evaluate_explanation(node, content, previous=previous)
        else:
            exercise = (node["quiz"] or {}).get("exercise", {})
            evaluation = writer.evaluate_exercise(
                node, exercise, content, previous=previous,
                learner_context=_learner_context(learner))
    except RuntimeError:
        raise HTTPException(503, "no pudimos evaluar tu entrega ahora, intenta de nuevo en un momento")
    # Calibration only makes sense against a number — explains have none.
    if body.kind != "explain" and body.predicted is not None and 0 <= body.predicted <= 100:
        evaluation["predicted"] = body.predicted
    with db.connect() as conn:
        sub = db.add_submission(conn, learner["id"], body.kind, content,
                                evaluation, node_id=node["id"],
                                prompt=_prompt_snapshot(body.kind, node=node))
        conn.commit()
    out = _evaluation_out(sub, attempt=prior_attempts + 1)
    # What they keep, not just what this attempt scored. Retrying is only
    # risk-free if the screen says so (docs/02) — the database always honoured
    # it, the UI never showed it.
    this_score = _final_score(sub.get("evaluation") or {})
    out["best_score"] = max([s for s in (best_before, this_score) if s is not None],
                            default=None)
    return {"ok": True, "evaluation": out}


class ReteachBody(BaseModel):
    node_id: int


@router.post("/reteach")
def reteach(body: ReteachBody, learner_session: str | None = Cookie(default=None)):
    """Teach the concept again, differently, when the learner did not get it.

    The explain step diagnoses ("todavía no" + what is missing) and used to stop
    there, which leaves someone who genuinely did not understand with only two
    moves: retry with the same understanding, or skip. This is the third move.

    Not stored: it is help, not work. Nothing here is evaluated, nothing counts
    toward the portfolio, and asking for it can never lower a score — the whole
    point is that admitting you are lost has to be safe.
    """
    learner = _require(learner_session)
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite por ahora, intenta más tarde")
    with db.connect() as conn:
        node, course, nodes = _node_with_course(conn, body.node_id)
        if not node:
            raise HTTPException(404, "lección no encontrada")
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        if node["id"] not in _accessible_for(
                conn, learner["id"], course, nodes, completed):
            raise HTTPException(403, "esta lección aún no está disponible")
        # Aim at the specific misunderstanding the evaluator already diagnosed,
        # if there is one. Without it this still works, just less pointedly.
        previous, _ = _previous_submission(
            conn, learner["id"], "explain", node_id=node["id"])
    ev = (previous or {}).get("evaluation") or {}
    try:
        out = writer.reteach_concept(
            node,
            learner_answer=(previous or {}).get("content", ""),
            misconception=ev.get("misconception"),
            missing=ev.get("missing"),
        )
    except RuntimeError:
        raise HTTPException(503, "no pudimos preparar la explicación ahora, intenta en un momento")
    if not out["explanation"]:
        raise HTTPException(503, "no pudimos preparar la explicación ahora, intenta en un momento")
    return {"ok": True, **out}


class DefendBody(BaseModel):
    submission_id: int
    answer: str


@router.post("/defend")
def defend(body: DefendBody, learner_session: str | None = Cookie(default=None)):
    """The ownership probe: answer the tutor's question about YOUR decisions.
    A good defense earns up to +10 on the submission's score. Retryable without
    limit — the BEST attempt is the one that counts, so defending again is
    always risk-free, and every evaluation says what a +10 answer would add."""
    learner = _require(learner_session)
    answer = " ".join(body.answer.split())
    if not 10 <= len(answer) <= 2000:
        raise HTTPException(400, "responde en 10 a 2000 caracteres")
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite de evaluaciones por ahora, intenta más tarde")
    with db.connect() as conn:
        sub = conn.execute(
            "SELECT * FROM submissions WHERE id = %s AND learner_id = %s",
            (body.submission_id, learner["id"])).fetchone()
        if not sub:
            raise HTTPException(404, "entrega no encontrada")
        ev = sub.get("evaluation") or {}
        if not ev.get("defense_question"):
            raise HTTPException(400, "esta entrega no tiene pregunta de defensa")
        if sub["node_id"]:
            node = conn.execute("SELECT title, objectives FROM syllabus_nodes WHERE id = %s",
                                (sub["node_id"],)).fetchone()
            context = f"Lección: {node['title']}. Objetivo: {node['objectives']}"
        else:
            cap = db.get_capstone(conn, sub["capstone_id"])
            context = f"Reto integrador: {cap['scenario'][:600]}"
    previous = ev.get("defense")
    try:
        result = writer.evaluate_defense(context, sub["content"],
                                         ev["defense_question"], answer,
                                         previous=previous)
    except RuntimeError:
        raise HTTPException(503, "no pudimos evaluar tu defensa ahora, intenta en un momento")
    import json as _json
    attempts = (ev.get("defense_attempts") or 0) + 1
    prev_best = ev.get("defense_best", (previous or {}).get("bonus", 0)) or 0
    best = max(result["bonus"], prev_best)
    # Show the feedback for what they just wrote; score with their best ever.
    ev["defense"] = {"question": ev["defense_question"], "answer": answer,
                     "bonus": result["bonus"], "comment": result["comment"],
                     "missing": result.get("missing") or []}
    # Keep the best ANSWER too: the document compiler quotes the learner's
    # reasoning, and it must quote their strongest one, not their latest.
    if result["bonus"] >= prev_best or not ev.get("defense_best_answer"):
        ev["defense_best_answer"] = answer
    ev["defense_attempts"] = attempts
    ev["defense_best"] = best
    ev["final_score"] = min(100, (ev.get("score") or 0) + best)
    with db.connect() as conn:
        conn.execute("UPDATE submissions SET evaluation = %s WHERE id = %s",
                     (_json.dumps(ev, ensure_ascii=False), sub["id"]))
        conn.commit()
        # The headline number is the learner's nota across this work item, not
        # the score of whichever submission they happened to defend. Defending an
        # older attempt must never pull the displayed score down.
        best_overall = db.best_score_for(
            conn, learner["id"], sub["kind"],
            node_id=sub["node_id"], capstone_id=sub["capstone_id"])
    return {"ok": True, "defense": ev["defense"], "attempts": attempts,
            "best": best, "final_score": ev["final_score"],
            "best_score": best_overall}


def _capstone_states(conn, course_id: int, learner_id: int) -> dict[int, dict]:
    """Per-module capstone rows with unlock/done state for one learner."""
    caps = db.course_capstones(conn, course_id)
    if not caps:
        return {}
    nodes = db.course_nodes(conn, course_id)
    prog = db.progress_map(conn, learner_id)
    completed = {nid for nid, p in prog.items() if p["completed_at"]}
    # docs/10: a declared skip opens its reto immediately. That is the whole
    # test-out path — the reto is a novel case the lessons never covered, so
    # passing it is evidence of the module's outcome contract in a way no CV is.
    exempt = db.exempt_modules_for(conn, learner_id, course_id)
    # Best attempt, never the latest: a weaker retry must not lower the score shown.
    latest = {s["capstone_id"]: s for s in db.best_submissions(conn, learner_id)
              if s["kind"] == "capstone" and s["capstone_id"]}
    out = {}
    for cap in caps:
        module_nodes = [n for n in nodes if n["module_no"] == cap["module_no"]]
        is_exempt = cap["module_no"] in exempt
        unlocked = bool(module_nodes) and (
            is_exempt or all(n["id"] in completed for n in module_nodes))
        sub = latest.get(cap["id"])
        ev = (sub or {}).get("evaluation") or {}
        out[cap["module_no"]] = {
            "id": cap["id"], "title": cap["title"],
            "status": "done" if sub else ("available" if unlocked else "locked"),
            "score": _final_score(ev),
            # The UI offers this as "pruébalo" rather than "reto" when it is the
            # test-out for a module they said they already know.
            "test_out": is_exempt and not sub,
        }
    return out


@router.get("/capstone/{capstone_id}")
def capstone(capstone_id: int, learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        cap = db.get_capstone(conn, capstone_id)
        if not cap:
            raise HTTPException(404, "reto no encontrado")
        course = conn.execute("SELECT * FROM courses WHERE id = %s", (cap["course_id"],)).fetchone()
        states = _capstone_states(conn, cap["course_id"], learner["id"])
        state = states.get(cap["module_no"], {})
        if state.get("status") == "locked":
            raise HTTPException(403, "termina las lecciones del módulo para desbloquear el reto")
        subs = [s for s in db.latest_submissions(conn, learner["id"])
                if s["kind"] == "capstone" and s["capstone_id"] == cap["id"]]
    return {
        "id": cap["id"], "course_slug": course["slug"], "module_no": cap["module_no"],
        "title": cap["title"], "scenario": cap["scenario"], "deliverable": cap["deliverable"],
        "last": _evaluation_out(subs[0]) if subs else None,
        "last_content": subs[0]["content"] if subs else "",
    }


class CapstoneBody(BaseModel):
    capstone_id: int
    content: str
    predicted: int | None = None


@router.post("/submit-capstone")
def submit_capstone(body: CapstoneBody, learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    content = body.content.strip()
    if not 50 <= len(content) <= 8000:
        raise HTTPException(400, "tu solución debe tener entre 50 y 8000 caracteres")
    with db.connect() as conn:
        cap = db.get_capstone(conn, body.capstone_id)
        if not cap:
            raise HTTPException(404, "reto no encontrado")
        states = _capstone_states(conn, cap["course_id"], learner["id"])
        if states.get(cap["module_no"], {}).get("status") == "locked":
            raise HTTPException(403, "termina las lecciones del módulo para desbloquear el reto")
        previous, prior_attempts = _previous_submission(
            conn, learner["id"], "capstone", capstone_id=cap["id"])
        # Same rule as /submit: identical text keeps its number (see there).
        if previous and (previous["content"] or "").strip() == content:
            out = _evaluation_out(previous, attempt=prior_attempts)
            out["unchanged"] = True
            out["best_score"] = db.best_score_for(
                conn, learner["id"], "capstone", capstone_id=cap["id"])
            return {"ok": True, "unchanged": True, "evaluation": out}
        best_before = db.best_score_for(
            conn, learner["id"], "capstone", capstone_id=cap["id"])
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite de evaluaciones por ahora, intenta más tarde")
    try:
        evaluation = writer.evaluate_capstone(cap, content, previous=previous)
    except RuntimeError:
        raise HTTPException(503, "no pudimos evaluar tu solución ahora, intenta de nuevo en un momento")
    if body.predicted is not None and 0 <= body.predicted <= 100:
        evaluation["predicted"] = body.predicted
    credited = None
    with db.connect() as conn:
        sub = db.add_submission(conn, learner["id"], "capstone", content,
                                evaluation, capstone_id=cap["id"],
                                prompt=_prompt_snapshot("capstone", capstone=cap))
        this_score = _final_score(sub.get("evaluation") or {})
        # docs/10 — the only path that converts a CLAIM into something that
        # counts. A reto is a novel case the lessons never covered, so passing it
        # is evidence of the module's outcome contract; a CV is not. Only a module
        # they had already declared can be credited: passing the reto after doing
        # the lessons is just a good reto score.
        if (this_score is not None and this_score >= writer.EXEMPTION_PASS_SCORE
                and cap["module_no"] in db.exempt_modules_for(
                    conn, learner["id"], cap["course_id"])):
            row = db.credit_module_exemption(conn, learner["id"], cap["course_id"],
                                             cap["module_no"], sub["id"], this_score)
            credited = {"module_no": row["module_no"], "score": row["score"]}
        conn.commit()
    out = _evaluation_out(sub, attempt=prior_attempts + 1)
    out["best_score"] = max([s for s in (best_before, this_score) if s is not None],
                            default=None)
    return {"ok": True, "evaluation": out, "credited": credited}


# -------------------- portfolio case study (STAR) --------------------

MIN_CASE_STUDY_SUBMISSIONS = int(os.environ.get("MIN_CASE_STUDY_SUBMISSIONS", "3"))


def _feedback_with_defense(ev: dict) -> str:
    """Tutor feedback enriched with the learner's defense Q&A — the 'why' behind
    their decisions is gold for the document compilers."""
    fb = ev.get("feedback", "")
    d = ev.get("defense") or {}
    # Their strongest reasoning, not the most recent — this feeds the deliverable.
    answer = ev.get("defense_best_answer") or d.get("answer")
    if answer:
        fb += f" | Defensa de la alumna — {d.get('question', '')}: {answer}"
    return fb


# Below this score the tutor judged there was no genuine attempt (a pasted
# starter prompt, an off-task line). Such a submission is not raw material: with
# nothing real to ground on, the compiler invents — it once produced a full
# skills inventory, tool list and English level for a learner whose only
# submission was the starter prompt with the placeholders still in it.
MIN_PORTFOLIO_SCORE = 25


def _is_real_work(s: dict) -> bool:
    ev = s.get("evaluation") or {}
    # `final_score` is often PRESENT but null (no defensa answered yet), so
    # dict.get's default never fires — an earlier version of this used
    # ev.get("final_score", ev.get("score")) and silently rejected the design partner's real
    # 55-point work. Coalesce on the value, not on key presence.
    score = ev.get("final_score")
    if score is None:
        score = ev.get("score")
    try:
        return float(score) >= MIN_PORTFOLIO_SCORE
    except (TypeError, ValueError):
        return False        # unscored work product: don't feed the compiler


def _course_submissions(conn, learner_id: int, course_id: int) -> list[dict]:
    """The learner's strongest work in one course (exercises + capstones), in
    course order — the raw material for the document and the case study. Best,
    not latest: the compiled deliverable should show them at their best.

    Non-attempts are excluded (see MIN_PORTFOLIO_SCORE): a document compiled from
    nothing does not come out empty, it comes out fabricated."""
    rows = [s for s in db.best_submissions(conn, learner_id) if _is_real_work(s)]
    out = []
    for s in rows:
        if s["kind"] == "exercise" and s["node_id"]:
            node = conn.execute(
                "SELECT title, course_id, position FROM syllabus_nodes WHERE id = %s",
                (s["node_id"],)).fetchone()
            if node and node["course_id"] == course_id:
                ev = s.get("evaluation") or {}
                # The task AS ASKED when they answered it. The node's exercise is
                # regenerable; quoting today's version over yesterday's work would
                # misrepresent what they actually did.
                snap = s.get("prompt_snapshot") or {}
                out.append({"kind": "ejercicio",
                            "title": snap.get("lesson_title") or node["title"],
                            "order": node["position"],
                            "task": snap.get("instruction", ""),
                            "content": s["content"], "feedback": _feedback_with_defense(ev)})
        elif s["kind"] == "capstone" and s["capstone_id"]:
            cap = db.get_capstone(conn, s["capstone_id"])
            if cap and cap["course_id"] == course_id:
                ev = s.get("evaluation") or {}
                out.append({"kind": "reto integrador", "title": cap["title"],
                            "order": 100 + cap["module_no"],
                            "content": s["content"], "feedback": _feedback_with_defense(ev)})
    return sorted(out, key=lambda x: x["order"])


def _route_submissions(conn, learner_id: int, analysis: dict) -> list[dict]:
    """The learner's strongest work across every course in their route, tagged
    with the course it came from — the raw material for the goal document.
    Route order (núcleo first), then course order within each."""
    out = []
    for r in (analysis.get("ruta") or []):
        c = conn.execute("SELECT * FROM courses WHERE slug = %s",
                         (r["course_slug"],)).fetchone()
        if not c:
            continue
        for it in _course_submissions(conn, learner_id, c["id"]):
            out.append({**it, "course_title": c["title"]})
    return out


@router.get("/case-study/{slug}")
def case_study_status(slug: str, learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        c = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
        if not c:
            raise HTTPException(404, "curso no encontrado")
        cs = db.get_case_study(conn, learner["id"], c["id"])
        subs = _course_submissions(conn, learner["id"], c["id"])
    return {
        "exists": bool(cs),
        "eligible": len(subs) >= MIN_CASE_STUDY_SUBMISSIONS,
        "submissions": len(subs), "needed": MIN_CASE_STUDY_SUBMISSIONS,
        "title": cs["title"] if cs else "",
        "content_md": cs["content_md"] if cs else "",
        "share_url": f"/aprende/caso/{cs['share_token']}" if cs else "",
    }


@router.post("/case-study/{slug}")
def generate_case_study(slug: str, learner_session: str | None = Cookie(default=None)):
    """Compose (or refresh) the learner's STAR portfolio case study from their
    real submissions in this course. The share link stays stable."""
    learner = _require(learner_session)
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite de evaluaciones por ahora, intenta más tarde")
    with db.connect() as conn:
        c = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
        if not c:
            raise HTTPException(404, "curso no encontrado")
        subs = _course_submissions(conn, learner["id"], c["id"])
        if len(subs) < MIN_CASE_STUDY_SUBMISSIONS:
            raise HTTPException(
                400, f"envía al menos {MIN_CASE_STUDY_SUBMISSIONS} trabajos (ejercicios o retos) "
                     "de este curso para armar tu caso de estudio")
        existing = db.get_case_study(conn, learner["id"], c["id"])
    name = learner["name"] or learner["email"].split("@")[0]
    try:
        result = writer.compose_case_study(c["title"], name, subs)
    except RuntimeError:
        raise HTTPException(503, "no pudimos generar tu caso de estudio ahora, intenta en un momento")
    token = existing["share_token"] if existing else secrets.token_urlsafe(12)
    with db.connect() as conn:
        cs = db.upsert_case_study(conn, learner["id"], c["id"],
                                  result["title"], result["content_md"], token)
        conn.commit()
    return {"ok": True, "title": cs["title"], "content_md": cs["content_md"],
            "share_url": f"/aprende/caso/{cs['share_token']}"}


@router.get("/project-doc/{slug}")
def project_doc_status(slug: str, learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        c = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
        if not c:
            raise HTTPException(404, "curso no encontrado")
        doc = db.get_project_doc(conn, learner["id"], c["id"])
        subs = _course_submissions(conn, learner["id"], c["id"])
    tpl = writer.PROJECT_TEMPLATES.get(slug, writer.PROJECT_TEMPLATES["default"])
    return {
        "exists": bool(doc),
        "eligible": len(subs) >= MIN_CASE_STUDY_SUBMISSIONS,
        "submissions": len(subs), "needed": MIN_CASE_STUDY_SUBMISSIONS,
        "doc_type": tpl["doc_type"],
        "title": doc["title"] if doc else "",
        "content_md": doc["content_md"] if doc else "",
        "share_url": f"/aprende/doc/{doc['share_token']}" if doc else "",
    }


@router.post("/project-doc/{slug}")
def generate_project_doc(slug: str, learner_session: str | None = Cookie(default=None)):
    """Compile the learner's submissions into the course's client-grade
    deliverable. Regenerable as they progress; share link stays stable."""
    learner = _require(learner_session)
    if not _eval_rate_ok(learner["id"]):
        raise HTTPException(429, "alcanzaste el límite de evaluaciones por ahora, intenta más tarde")
    with db.connect() as conn:
        c = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
        if not c:
            raise HTTPException(404, "curso no encontrado")
        subs = _course_submissions(conn, learner["id"], c["id"])
        if len(subs) < MIN_CASE_STUDY_SUBMISSIONS:
            raise HTTPException(
                400, f"envía al menos {MIN_CASE_STUDY_SUBMISSIONS} trabajos de este curso "
                     "para compilar tu documento")
        existing = db.get_project_doc(conn, learner["id"], c["id"])
    name = learner["name"] or learner["email"].split("@")[0]
    try:
        result = writer.compose_project_doc(slug, c["title"], name, subs)
    except RuntimeError:
        raise HTTPException(503, "no pudimos compilar tu documento ahora, intenta en un momento")
    token = existing["share_token"] if existing else secrets.token_urlsafe(12)
    with db.connect() as conn:
        doc = db.upsert_project_doc(conn, learner["id"], c["id"],
                                    result["title"], result["content_md"], token)
        conn.commit()
    return {"ok": True, "title": doc["title"], "content_md": doc["content_md"],
            "share_url": f"/aprende/doc/{doc['share_token']}"}


@router.get("/doc/{token}")
def public_project_doc(token: str):
    """Public JSON for any shared paper document (course doc or goal doc) —
    no auth, the token is the capability. One page serves both; only the
    credit line differs."""
    with db.connect() as conn:
        doc = db.doc_by_token(conn, token)
    if not doc:
        raise HTTPException(404, "documento no encontrado")
    credit = (f"Documento elaborado por {doc['learner_name']} durante el curso "
              f"«{doc['context']}»" if doc["kind"] == "course" else
              f"Documento elaborado por {doc['learner_name']} con su trabajo real, "
              f"orientado al puesto «{doc['context']}»")
    return {"title": doc["title"], "content_md": doc["content_md"],
            "learner_name": doc["learner_name"], "course_title": doc["context"],
            "credit": credit,
            "updated_at": doc["updated_at"].date().isoformat()}


@router.get("/caso/{token}")
def public_case_study(token: str):
    """Public JSON for a shared case study — no auth, token is the capability."""
    with db.connect() as conn:
        cs = db.case_study_by_token(conn, token)
    if not cs:
        raise HTTPException(404, "caso no encontrado")
    return {"title": cs["title"], "content_md": cs["content_md"],
            "learner_name": cs["learner_name"], "course_title": cs["course_title"],
            "updated_at": cs["updated_at"].date().isoformat()}


@router.get("/portfolio")
def portfolio(learner_session: str | None = Cookie(default=None)):
    """Everything the learner has produced, with evaluations — 'Mi trabajo'."""
    learner = _require(learner_session)
    with db.connect() as conn:
        rows = db.learner_portfolio(conn, learner["id"])
    out = []
    for r in rows:
        ev = r.get("evaluation") or {}
        out.append({
            "kind": r["kind"],
            "title": r["capstone_title"] if r["kind"] == "capstone" else (r["node_title"] or ""),
            "course_slug": r.get("course_slug") or "",
            "course_title": r.get("course_title") or "",
            "content": r["content"],
            # Explains never show a number — not even legacy ones scored under
            # the old rubric, whose values are not comparable to anything.
            "score": None if (ev.get("verdict") or r["kind"] == "explain") else _final_score(ev),
            "verdict": ev.get("verdict"),
            "feedback": ev.get("feedback", ""),
            "created_at": r["created_at"].date().isoformat(),
        })
    return {"items": out}


MAX_OPEN_REQUESTS = int(os.environ.get("MAX_OPEN_REQUESTS", "3"))

# Learner-facing status labels for course requests (concierge pipeline).
REQUEST_LABELS = {
    "new": "Recibida",
    "reviewing": "En revisión",
    "building": "En producción",
    "published": "Disponible",
    "rejected": "Descartada",
}


def _request_out(row: dict) -> dict:
    return {
        "id": row["id"],
        "topic": row["topic"],
        "detail": row["detail"],
        "status": row["status"],
        "status_label": REQUEST_LABELS.get(row["status"], row["status"]),
        "course_slug": row["course_slug"] if row["status"] == "published" else None,
        "created_at": row["created_at"].date().isoformat(),
    }


class RequestBody(BaseModel):
    topic: str
    detail: str = ""


@router.post("/request")
def create_request(body: RequestBody, learner_session: str | None = Cookie(default=None)):
    """Course concierge: a learner asks for a course on a topic. Capped at a few
    open requests per learner so the queue stays a demand signal, not a dump."""
    learner = _require(learner_session)
    topic = " ".join(body.topic.split())
    detail = " ".join(body.detail.split())[:1000]
    if not 5 <= len(topic) <= 200:
        raise HTTPException(400, "cuéntanos el tema en 5 a 200 caracteres")
    with db.connect() as conn:
        if db.open_request_count(conn, learner["id"]) >= MAX_OPEN_REQUESTS:
            raise HTTPException(
                400, "ya tienes solicitudes en proceso — espera a que terminemos esas")
        row = db.create_course_request(conn, learner["id"], topic, detail)
        conn.commit()
    return {"ok": True, "request": _request_out(row)}


@router.get("/requests")
def my_requests(learner_session: str | None = Cookie(default=None)):
    learner = _require(learner_session)
    with db.connect() as conn:
        rows = db.learner_requests(conn, learner["id"])
    return {"requests": [_request_out(r) for r in rows]}


class CompleteBody(BaseModel):
    node_id: int
    quiz_score: float  # 0..1
    # Accepted for backwards compatibility with older clients, but IGNORED: the
    # server decides what is a review. See the handler.
    is_review: bool = False


@router.post("/complete")
def complete(body: CompleteBody, learner_session: str | None = Cookie(default=None)):
    """Record a completion. Everything the client sends here is untrusted.

    This endpoint used to write progress for ANY node_id with no access check,
    which was the whole progression gate: access is DERIVED from completions
    (`_accessible_ids`), so writing a completion writes access. Posting one
    request per lesson unlocked the entire catalog and its videos. It also
    stored `quiz_score` unclamped — and `record_completion` keeps the GREATEST
    score, so a single bogus value was permanent.

    Three rules, all server-side (docs/07: server decides state, client only
    displays it):
      1. the node must exist and be accessible to THIS learner;
      2. quiz_score is clamped to the 0..1 the contract always claimed;
      3. is_review is derived from whether they already completed it — never
         taken from the request body, which could silently downgrade a real
         first completion into a review.
    """
    learner = _require(learner_session)
    quiz_score = min(1.0, max(0.0, float(body.quiz_score)))
    with db.connect() as conn:
        node, course, nodes = _node_with_course(conn, body.node_id)
        if not node:
            raise HTTPException(404, "lección no encontrada")
        prog = db.progress_map(conn, learner["id"])
        completed = {nid for nid, p in prog.items() if p["completed_at"]}
        if node["id"] not in _accessible_for(
                conn, learner["id"], course, nodes, completed):
            raise HTTPException(403, "esta lección aún no está disponible")
        # A review is a lesson they have ALREADY completed — that is a fact in
        # the database, not a claim the client gets to make.
        if node["id"] in completed:
            db.record_review(conn, learner["id"], node["id"], quiz_score)
        else:
            db.record_completion(conn, learner["id"], node["id"], quiz_score)
        conn.commit()
        streak = db.streak_days(conn, learner["id"])
    return {"ok": True, "streak": streak}
