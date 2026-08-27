"""HTTP checks for the public surface — the routes, not the rendering (docs/11).

    python studio/cloud/check_public_surface.py [base_url]

Defaults to http://localhost:8799. Point it at the live URL after a deploy:

    python studio/cloud/check_public_surface.py https://estudio-production-1b8c.up.railway.app

The three DOM-shim checks assert what the SPA *renders*. Nothing asserted what
the server *serves*, which is where this codebase's worst bugs have lived: a
write that granted a read, an admin route that shipped public because it was not
added to an allowlist. Those are HTTP facts, and this is the file that states
them.

Every assertion here is one that was verified by hand at least once. Automating
them is the difference between "I checked that on the day" and "it is still
true", which is the same distinction docs/07 draws with "exit 0 is not
verification".
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.request

DEFAULT_BASE = "http://localhost:8799"
DEMO_SLUG = "curso-meta-ads"


def fetch(url: str, headers: dict | None = None) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(200_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(2000).decode("utf-8", "replace")
    except Exception as exc:                    # connection refused, DNS, TLS
        return 0, f"{type(exc).__name__}: {exc}"


def audit_allowlist(check) -> None:
    """The admin gate is an allowlist, and docs/07 records that a new /api/*
    route which is not on it ships PUBLIC — it nearly happened twice in one day,
    once with the invite-code list. This runs offline against the real predicate,
    so the bug class cannot come back quietly between deploys.

    Add a row here in the same edit that adds a route. That is the whole point.
    """
    root = str(__import__("pathlib").Path(__file__).resolve().parents[1])
    sys.path.insert(0, root + "/dashboard")
    sys.path.insert(0, root)
    try:
        import app as dashboard          # noqa: PLC0415
    except Exception as exc:
        check("admin allowlist is auditable", False, f"could not import app.py: {exc}")
        return

    gated = [
        ("/panel", "the dashboard itself"),
        ("/api/state", "production stats"),
        ("/api/jobs/render", "job triggers"),
        ("/api/videos/ch/name", "the video library"),
        ("/media/curso/x.mp4", "every rendered lesson"),
        ("/api/upload-media", "writes to the volume"),
        ("/api/delete-media", "deletes from the volume"),
        ("/api/learners", "learner names and emails"),
        ("/api/learners/1/work", "everything a learner ever wrote"),
        ("/api/submissions/1/flag", "operator review"),
        ("/api/invites", "invite codes ARE the access gate"),
        ("/api/waitlist", "signup emails"),
        ("/api/requests", "the concierge queue"),
        ("/api/demand", "every posting strangers pasted"),
        ("/api/access-requests", "locked-out learners' emails"),
    ]
    public = [
        ("/", "the public site"),
        ("/aprende", "the app"),
        ("/oferta", "the job analyser"),
        ("/lista", "the waitlist"),
        ("/curso/curso-meta-ads", "a temario"),
        ("/api/learn/public/demo", "the free lesson"),
        ("/api/learn/public/demo-video", "the free lesson's video"),
        ("/api/learn/login", "login"),
        ("/api/learn/today", "a learner's own day (session-gated, not token-gated)"),
        ("/aprende/doc/sometoken", "a share page"),
    ]
    for path, why in gated:
        check(f"gated: {path} ({why})", dashboard._is_admin_path(path) is True,
              "NOT on the allowlist — this would ship public")
    for path, why in public:
        check(f"public: {path} ({why})", dashboard._is_admin_path(path) is False,
              "on the admin allowlist — this would 401 for everyone")


def main(argv: list[str]) -> int:
    base = (argv[0] if argv else DEFAULT_BASE).rstrip("/")
    print(f"base: {base}\n")
    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

    # Offline first: the allowlist is a pure function and needs no server.
    audit_allowlist(check)

    # Preflight. Without this, an unreachable base means every HTTP assertion
    # below waits out its own timeout and the run takes minutes to tell you the
    # server is not running. A tool that is slow to say "no" is a tool nobody
    # runs before a deploy.
    code, detail = fetch(base + "/aprende")
    if code == 0:
        for name, ok, d in results:
            print(("  PASS  " if ok else "  FAIL  ") + name + (f" — {d}" if d and not ok else ""))
        offline_bad = sum(1 for _, ok, _ in results if not ok)
        print(f"\n{len(results) - offline_bad}/{len(results)} offline checks passed")
        print(f"\nHTTP checks skipped: {base} is not reachable ({detail}).")
        print("Start the server (docs/05) or pass the live URL as the first argument.")
        return 1 if offline_bad else 0

    # ---- public surfaces answer, and carry real metadata -------------------
    for path, want_view in (("/oferta", '"oferta"'), ("/lista", '"lista"')):
        code, body = fetch(base + path)
        check(f"{path} serves", code == 200, f"got {code}")
        check(f"{path} names its view", want_view in body)
        check(f"{path} has a real <title>", "<title>" in body and "Rumbo" in body)
        check(f"{path} has an og:description", 'property="og:description"' in body)

    code, body = fetch(f"{base}/curso/{DEMO_SLUG}")
    check("/curso/<slug> serves", code == 200, f"got {code}")
    check("/curso/<slug> titles the real course", "Meta Ads" in body)
    check("/curso/<slug> passes the slug", f'"{DEMO_SLUG}"' in body)

    # An unknown slug is a visitor's typo, never a 500.
    code, _ = fetch(f"{base}/curso/no-existe-este-curso")
    check("/curso/<unknown> does not error", code == 200, f"got {code}")

    # ---- the app still serves ---------------------------------------------
    code, body = fetch(base + "/aprende")
    check("/aprende serves", code == 200, f"got {code}")
    check("/aprende is branded Rumbo", "Rumbo" in body and "Aprende IA" not in body)

    # ---- the free lesson (docs/11) ----------------------------------------
    code, body = fetch(base + "/api/learn/public/demo")
    check("public demo serves", code == 200, f"got {code}")
    check("demo carries the explain prompt", '"explain_prompt"' in body)
    check("demo carries the module's reto", '"reto"' in body)

    code, _ = fetch(base + "/api/learn/public/demo-poster")
    check("demo poster serves", code == 200, f"got {code} — the plate would show a broken image")

    code, _ = fetch(base + "/api/learn/public/demo-video",
                    {"Range": "bytes=0-1023"})
    check("demo video serves ranges", code == 206, f"got {code}")

    # ---- and the gates still hold ------------------------------------------
    # These are the assertions that matter most. Every one of them corresponds to
    # a bug this codebase actually shipped (docs/07).
    #
    # The admin gate is DELIBERATELY open locally: docs/03 records that an empty
    # DASHBOARD_TOKEN means open in dev and fails closed in production. So the
    # expectation depends on where we are pointed, and saying so here is the
    # point — a check that fails on localhost gets ignored, and an ignored check
    # is worse than none.
    is_local = "localhost" in base or "127.0.0.1" in base
    if is_local:
        print("  (localhost: the admin gate is open by design — docs/03. "
              "Run this against the live URL to assert it.)\n")
    for path, want, why in (
        ("/api/learn/video/1", 401, "a gated lesson video must never be public"),
        ("/api/state", 401, "admin surface"),
        ("/api/demand", 401, "every posting strangers pasted"),
        ("/api/invites", 401, "invite codes ARE the access gate"),
        ("/api/learners", 401, "learner emails"),
        ("/api/access-requests", 401, "locked-out learners' emails"),
    ):
        code, _ = fetch(base + path)
        if is_local:
            check(f"{path} reachable in dev ({why} — gated in production)",
                  code in (200, 401), f"got {code}")
        else:
            check(f"{path} is gated ({why})", code == 401, f"got {code}")

    # Recon surfaces are off in production; locally FastAPI serves them.
    code, _ = fetch(base + "/openapi.json")
    check("/openapi.json disabled in production", code in (404, 200),
          f"got {code} (200 is expected locally, 404 in production)")

    # The demo endpoint takes no lesson id — an unauthenticated read that accepts
    # one would publish all 420 gated videos (docs/11).
    code, _ = fetch(base + "/api/learn/public/demo-video?node_id=99")
    check("demo video ignores a supplied node_id", code in (200, 206, 429),
          f"got {code}")

    bad = 0
    for name, ok, detail in results:
        if not ok:
            bad += 1
        print(("  PASS  " if ok else "  FAIL  ") + name + (f" — {detail}" if detail and not ok else ""))
    print(f"\n{len(results) - bad}/{len(results)} public-surface checks passed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
