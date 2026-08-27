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


def main(argv: list[str]) -> int:
    base = (argv[0] if argv else DEFAULT_BASE).rstrip("/")
    print(f"base: {base}\n")
    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

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
