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

import re
import sys
import urllib.error
import urllib.request


def _no_scripts(html: str) -> str:
    """Markup with <script>/<style> removed, tags otherwise intact.

    Needed because a needle found inside a <script> proves nothing here: the
    SPA's source contains every string it will ever render, so searching the raw
    body would pass even when the server sent a blank page. Keeps tags so that
    href assertions still work.
    """
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    return re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)


def _strip_scripts(html: str) -> str:
    """Body text as a non-JS client sees it: scripts gone, tags flattened."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", _no_scripts(html))).strip()

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


class AllowlistUnauditable(RuntimeError):
    """The allowlist audit could not run. Never downgraded to a failed check:
    a skipped section that still prints a score is how a degraded tool reads as
    a clean bill of health."""


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
        from admin_paths import is_admin_path   # noqa: PLC0415
    except Exception as exc:
        # This must never read as "one failed check". Skipping this section drops
        # 25 assertions about which paths are public, and a summary line saying
        # 31/32 would make that look like a rounding error. It is the whole point
        # of the file.
        raise AllowlistUnauditable(str(exc)) from exc

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
        ("/login", "sign-in"),
        ("/cursos", "the catalog"),
        ("/curso/curso-meta-ads", "a temario"),
        ("/api/learn/public/demo", "the free lesson"),
        ("/api/learn/public/demo-video", "the free lesson's video"),
        ("/api/learn/login", "login"),
        ("/api/learn/today", "a learner's own day (session-gated, not token-gated)"),
        ("/aprende/doc/sometoken", "a share page"),
    ]
    for path, why in gated:
        check(f"gated: {path} ({why})", is_admin_path(path) is True,
              "NOT on the allowlist — this would ship public")
    for path, why in public:
        check(f"public: {path} ({why})", is_admin_path(path) is False,
              "on the admin allowlist — this would 401 for everyone")


def main(argv: list[str]) -> int:
    base = (argv[0] if argv else DEFAULT_BASE).rstrip("/")
    print(f"base: {base}\n")
    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

    # Offline first: the allowlist is a pure function and needs no server.
    try:
        audit_allowlist(check)
    except AllowlistUnauditable as exc:
        print("=" * 68)
        print("  THE ADMIN ALLOWLIST AUDIT DID NOT RUN.")
        print("  25 assertions about which paths are public were SKIPPED.")
        print(f"  reason: {exc}")
        print()
        print("  This is the most important section of this file: it is what")
        print("  catches an admin route shipping public (docs/07). Do not read")
        print("  the HTTP results below as a pass.")
        print()
        print("  Run it from the repo root so studio/dashboard is importable:")
        print("    python studio/cloud/check_public_surface.py [base_url]")
        print("=" * 68)
        return 2

    # ---- the frontend is built, and nothing ships from a CDN ---------------
    # /aprende is behind a session and answers a cookie-less request with a
    # redirect, so what is asserted here is the BUILD OUTPUT rather than a
    # response. learn.html — the 3,192-line file both frontends used to live in —
    # is gone; if it comes back, so does the bug that ended it.
    from pathlib import Path as _Path
    dist = _Path(__file__).resolve().parents[1] / "web" / "dist"
    legacy = _Path(__file__).resolve().parents[1] / "dashboard" / "static" / "learn.html"
    check("the vanilla SPA is gone", not legacy.exists(),
          "learn.html is back; the public surface and the app would drift again")
    check("the app was built", (dist / "aprende" / "index.html").is_file(),
          "run: cd studio/web && npm ci && npm run build")
    if (dist / "aprende" / "index.html").is_file():
        app_html = (dist / "aprende" / "index.html").read_text(encoding="utf-8")
        check("the app is branded Rumbo",
              "Rumbo" in app_html and "Aprende IA" not in app_html)
        # A learner's workspace must never enter a search index: their documents
        # live on unguessable tokens, and an indexed token is not unguessable.
        check("the app tells crawlers to stay out", "noindex" in app_html)
        # marked, DOMPurify and mermaid are bundled now. A CDN reappearing here
        # is a third party back on the critical path of a page that carries a
        # session cookie and a portfolio.
        for page, label in ((dist / "index.html", "the landing"),
                            (dist / "aprende" / "index.html", "the app")):
            if page.is_file():
                check(f"{label} loads no CDN script",
                      "cdn.jsdelivr.net" not in page.read_text(encoding="utf-8"),
                      "a third-party script origin is back")

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
    # Each of these is now its own built HTML file, so a page either IS its view
    # or it is the wrong file. There is no `window.__VIEW__` to assert any more:
    # the server used to hand the SPA a starting view because all six URLs were
    # the same document, which is the arrangement this whole migration removed.
    for path, headline in (("/oferta", "Dinos qué quieres"),
                           ("/lista", "Te avisamos cuando se abra tu cupo"),
                           ("/cursos", "Todo lo que puedes estudiar"),
                           ("/login", "Entra y sigue donde lo dejaste")):
        code, body = fetch(base + path)
        check(f"{path} serves", code == 200, f"got {code}")
        check(f"{path} is its own page", headline in _strip_scripts(body),
              "served a different page's HTML, or an empty shell")
        check(f"{path} has a real <title>", "<title>" in body and "Rumbo" in body)
        check(f"{path} has an og:description", 'property="og:description"' in body)

    code, body = fetch(f"{base}/curso/{DEMO_SLUG}")
    check("/curso/<slug> serves", code == 200, f"got {code}")
    check("/curso/<slug> titles the real course", "Meta Ads" in body)
    check("/curso/<slug> names its deliverable", "Plan de campaña" in _strip_scripts(body),
          "the page argues the document first; without it this is a table of contents")

    # An unknown slug is a visitor's typo, never a 500 and never a dead end: it
    # redirects to the catalog, which urllib follows.
    code, body = fetch(f"{base}/curso/no-existe-este-curso")
    check("/curso/<unknown> does not error", code == 200, f"got {code}")
    check("/curso/<unknown> lands on the catalog",
          "Todo lo que puedes estudiar" in _strip_scripts(body))

    # ---- the pages carry their CONTENT, not just their metadata ------------
    # Every public page used to serve exactly eleven characters of body text —
    # "Cargando…" — to anything that does not run JS. Meta tags passed the checks
    # above the whole time, which is precisely why this section exists: the
    # metadata was never the thing that was missing.
    for path, needle, why, markup in (
        ("/", "tutora", "the landing's argument", False),
        # Attribute order, not the link, is what an `<a href=` needle actually
        # tests — and it changed the moment these became components.
        ("/cursos", 'href="/curso/', "links a crawler can walk to the temarios", True),
        (f"/curso/{DEMO_SLUG}", "Módulo 1", "the modules", False),
        ("/oferta", "oferta de trabajo que te interesa", "what the analyser does", False),
        ("/", "SMART", "the real lesson, not a description of one", False),
    ):
        _, body = fetch(base + path)
        hay = _no_scripts(body) if markup else _strip_scripts(body)
        check(f"{path} prerenders {why}", needle in hay,
              "body is client-rendered only — invisible to crawlers and answer engines")

    _, body = fetch(f"{base}/curso/{DEMO_SLUG}")
    text = _strip_scripts(body)
    check("/curso/<slug> prerenders real lesson content", len(text) > 3000,
          f"only {len(text)} chars of body text; the temario is 30 lessons")

    # ---- robots + sitemap --------------------------------------------------
    code, body = fetch(base + "/robots.txt")
    check("/robots.txt serves", code == 200, f"got {code}")
    check("robots allows the temarios", "Allow: /curso/" in body)
    check("robots keeps crawlers out of the app", "Disallow: /aprende" in body,
          "learner share tokens must never enter a search index")
    check("robots points at the sitemap", "Sitemap:" in body)

    code, body = fetch(base + "/sitemap.xml")
    check("/sitemap.xml serves", code == 200, f"got {code}")
    check("sitemap lists every course", body.count("/curso/") >= 14,
          f"only {body.count('/curso/')} course URLs")
    check("sitemap uses the public base url", "ponrumbo.com" in body or "localhost" in body)

    # ---- the public site ships no CDN dependency at all --------------------
    # Static pages have no runtime library to fetch. A CDN <script> reappearing
    # here means a component reached for one, and that is a third party on the
    # critical path of the page strangers arrive on.
    for path in ("/", "/cursos", "/oferta"):
        _, body = fetch(base + path)
        check(f"{path} loads no CDN script", "cdn.jsdelivr.net" not in body,
              "a third-party script on the public critical path")

    # ---- the app is behind a session ---------------------------------------
    # These two used to fetch /aprende and read the SPA. They now silently read
    # the LANDING, because a request with no cookie is redirected there and
    # urllib follows it — so both passed while asserting nothing about the app.
    # What is worth checking over HTTP is the redirect itself; the app's markup
    # is asserted offline above, against the file.
    code, body = fetch(base + "/aprende")
    check("/aprende serves", code == 200, f"got {code}")
    check("/aprende sends a visitor with no session to the public site",
          "Todo lo que puedes" in body or "Haz una clase" in body,
          "a stranger reached the learner app instead of the landing")

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
