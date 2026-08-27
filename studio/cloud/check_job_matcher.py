"""Calibration harness for the job-posting matcher (docs/08-job-target.md).

Run this before shipping ANY change to JOB_MATCH_SYSTEM, JOB_JSON_SPEC or
_normalise_job_analysis. Prompt changes have no other regression test, and the
failure mode is silent: the matcher quietly starts flattering our own catalog.

    DATABASE_URL=... OPENROUTER_API_KEY=... LLM_MODEL=... \
        python studio/cloud/check_job_matcher.py

Exits non-zero if any fixture fails its expectations. The full analysis is
printed either way — reading it is the point; the assertions only catch the
regressions we already know how to name.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cloud import db, writer  # noqa: E402

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "job-postings"


def _words(*parts: str) -> set[str]:
    """Lowercased word set. Substring matching here once let 'Redacción' satisfy
    an assertion looking for 'red' (social media) — a silent false PASS."""
    return set(re.findall(r"\w+", " ".join(parts).lower()))


def _check_real(a: dict) -> list[str]:
    """the design partner's real posting: broad marketing role, one true gap, ads kept shallow.

    NOTE: an earlier version of this fixture expected organic social-media
    management to come back as a gap. Reading the catalog disproved it —
    curso-marketing-ia M3 covers "posts para redes ... planificarás un mes entero
    de contenido", which is what the posting actually asks for. The expectation
    was wrong, not the matcher. Fixtures answer to the data, not the reverse.
    """
    fails = []
    slugs = {r["course_slug"]: r["through_module"] for r in a["ruta"]}
    if not 60 <= a["coverage"] <= 95:
        fails.append(f"coverage {a['coverage']} outside 60-95 (broad but not total match)")
    for expected in ("curso-seo-aeo", "curso-email-marketing"):
        if expected not in slugs:
            fails.append(f"{expected} missing from route (posting names SEO/AEO and email flows)")
    if not a["gaps"]:
        fails.append("no gaps reported — posting demands planning tools we lack")
    gapwords = _words(*(f"{g.get('name','')} {g.get('evidence','')}" for g in a["gaps"]))
    if not gapwords & {"trello", "clickup", "notion", "planificación", "planificacion"}:
        fails.append("planning tools (Trello/ClickUp/Notion) not reported as a gap")
    # Baseline traits and experience requirements are not teachable competencies;
    # listing them inflates gaps and makes the role look unreachable.
    compwords = _words(*(c.get("name", "") for c in a["competencies"]))
    if compwords & {"ortografía", "ortografia", "gramática", "gramatica", "años", "anos"}:
        fails.append("baseline traits / experience requirements leaked into competencies")
    # The posting explicitly excludes budget ownership, so the ads courses must
    # stop before their bidding/budget module. Over-prescribing depth is the same
    # failure as over-claiming coverage.
    for ads in ("curso-google-ads", "curso-meta-ads", "curso-tiktok-ads"):
        if slugs.get(ads, 0) == 5:
            fails.append(f"{ads} routed through module 5 — posting says the role "
                         f"does not manage ad budget")
    # A plan someone cannot start is not a plan. The full honest route for this
    # posting is ~120 lessons and that is CORRECT — the posting really does
    # demand that much, and truncating it would be a lie about readiness. So the
    # constraint is on the núcleo, which is WHERE YOU START (max 2 courses), not
    # the job-readiness bar. Defining it as readiness put 84 of 126 lessons in
    # the núcleo, which no stranger on a landing page ever begins.
    if not 12 <= a["core_lessons"] <= 60:
        fails.append(f"núcleo is {a['core_lessons']} lessons — should be a startable "
                     f"block of at most 2 courses (12-60)")
    if a["ruta"] and a["ruta"][0]["phase"] != "nucleo":
        fails.append("route does not lead with the núcleo")
    if not a["doc_type"]:
        fails.append("no document target on a well-covered posting")
    return fails


def _check_adversarial(a: dict) -> list[str]:
    """A senior data-engineering role. The only correct answer is 'not us'."""
    fails = []
    if a["coverage"] > 20:
        fails.append(f"coverage {a['coverage']} > 20 on an out-of-coverage role")
    if len(a["ruta"]) > 1:
        fails.append(f"route has {len(a['ruta'])} courses — invented a marketing "
                     f"path through a data-engineering job")
    if not a["gaps"]:
        fails.append("no gaps reported on a job we cannot serve at all")
    # The first run refused the route but still promised a "Diseño de arquitectura
    # de pipeline de datos" with a pitch citing Spark and Terraform. Fabricating a
    # deliverable on an unauthenticated public page is the worst failure here.
    for field in ("doc_type", "doc_title", "pitch"):
        if a[field]:
            fails.append(f"fabricated {field} on a job we cannot serve: {a[field]!r}")
    return fails


def _check_budget_owner(a: dict) -> list[str]:
    """Performance Manager, Chile. The INVERSE of the design partner's posting: this role does
    own the ad budget, so the ads courses must run deep. If both postings return
    the same depth, the depth reasoning is a heuristic, not reasoning.
    """
    fails = []
    slugs = {r["course_slug"]: r["through_module"] for r in a["ruta"]}
    deep = [s for s in ("curso-meta-ads", "curso-google-ads", "curso-tiktok-ads")
            if slugs.get(s, 0) >= 5]
    if len(deep) < 2:
        fails.append("budget-owning role did not route at least two ads courses "
                     "through module 5 (the bidding/budget module)")
    # Looker Studio used to be asserted as a GAP here, and that assertion went
    # stale the day curso-analitica-marketing shipped: M5's own outcome contract
    # is "Transformarás GA4 + Sheets en un tablero de Looker Studio", lesson 27 is
    # named after it, and five lessons teach it. The matcher was right and the
    # fixture was wrong — the same shape docs/08 already records once ("Fixtures
    # answer to the catalog, not the reverse"), and it had been failing silently
    # ever since. The honest assertion is the inverse: a role that reports on
    # spend needs the reporting module, so calling it a gap is under-claiming.
    gapwords = _words(*(g.get("name", "") for g in a["gaps"]))
    if "looker" in gapwords:
        fails.append("Looker Studio called a gap — curso-analitica-marketing M5 "
                     "teaches it (lesson 27 is named after it)")
    if slugs.get("curso-analitica-marketing", 0) < 5:
        fails.append("a budget-owning role was not routed through the reporting "
                     "module that teaches Looker Studio")
    # This role's whole job is spending budget, and curso-google-ads M5 is
    # "Pujas, presupuesto y operación semanal". Calling it a gap while routing
    # short of M5 was the original under-claiming bug.
    if any("presupuesto" in _words(g.get("name", "")) for g in a["gaps"]) \
            and slugs.get("curso-google-ads", 0) < 5:
        fails.append("budget management called a gap while routing short of the "
                     "module that teaches it")
    return fails


def _check_adjacent(a: dict) -> list[str]:
    """App-install paid media. Adjacent to us and therefore the HARDEST honesty
    test: the platform mechanics are ours, the app/attribution layer is not.
    Both an empty route and a full-coverage claim are failures here.
    """
    fails = []
    if not a["ruta"]:
        fails.append("empty route — we do teach the ad platforms this role uses")
    if a["coverage"] > 75:
        fails.append(f"coverage {a['coverage']} > 75 on an app/attribution role")
    gapwords = _words(*(g.get("name", "") for g in a["gaps"]))
    for token, label in (("appsflyer", "AppsFlyer/attribution"),
                         ("sdks", "SDKs/deep links"),
                         ("app", "App Campaigns")):
        if token not in gapwords:
            fails.append(f"{label} not reported as a gap")
    return fails


def _invariants(a: dict, catalog: list[dict]) -> list[str]:
    """Properties that must hold for EVERY posting, whatever the role.

    These are the honesty guarantees the public page rests on. Each one is
    enforced in `_normalise_job_analysis`; this is the check that the enforcement
    is still there.
    """
    fails = []
    by_slug = {c["slug"]: c for c in catalog}
    for r in a["ruta"]:
        mods = set(r.get("modules") or [])
        if not mods:
            fails.append(f"{r['course_slug']}: empty modules list")
            continue
        if r["through_module"] != max(mods):
            fails.append(f"{r['course_slug']}: through_module ({r['through_module']}) "
                         f"!= max(modules) ({max(mods)})")
        course = by_slug.get(r["course_slug"])
        if course:
            # spec v2's whole point: every selected module's declared prereqs
            # must be in the selection (closure enforced server-side).
            closed = writer._close_over_prereqs(course, mods)
            if closed != mods:
                fails.append(f"{r['course_slug']}: modules {sorted(mods)} not "
                             f"prereq-closed (needs {sorted(closed - mods)})")
    if a["coverage"] == 100 and a["gaps"]:
        fails.append(f"claims 100% coverage while listing {len(a['gaps'])} gaps — "
                     f"the page would contradict itself")
    if not a["ruta"] and (a["doc_type"] or a["pitch"]):
        fails.append("promises a deliverable with an empty route")
    if a["coverage"] < writer.JOB_COVERAGE_FLOOR and a["doc_type"]:
        fails.append(f"promises a deliverable below the coverage floor "
                     f"({a['coverage']} < {writer.JOB_COVERAGE_FLOOR})")
    for r in a["ruta"]:
        for c in r["covers"]:
            if c["module_no"] > r["through_module"]:
                fails.append(f"{r['course_slug']} claims {c['competency']!r} from "
                             f"module {c['module_no']} but only routes to "
                             f"{r['through_module']}")
    if a["core_lessons"] > a["total_lessons"]:
        fails.append("núcleo larger than the whole route")
    return fails


def _check_goal_mode(a: dict) -> list[str]:
    """Goal intake (docs/09 item 4): a bare role name, no posting to cite. The
    role chosen is squarely covered by rendered courses, so an empty route or
    token coverage means the mode is broken — while the usual invariants
    (prereq closure, no fabricated doc) still apply via _invariants."""
    fails = []
    if not a["ruta"]:
        fails.append("empty route for a role the catalog squarely covers")
    if a["coverage"] < 30:
        fails.append(f"coverage {a['coverage']} < 30 on a well-covered role")
    slugs = {r["course_slug"] for r in a["ruta"]}
    if not slugs & {"curso-meta-ads", "curso-google-ads", "curso-tiktok-ads"}:
        fails.append("no ads course routed for a paid-media role")
    if not a["competencies"]:
        fails.append("no competencies extracted from the role")
    return fails


# (filename, label, check, mode) — mode "goal" exercises the no-posting intake.
CASES = [
    ("real-content-ecommerce-latam.txt", "REAL · content/e-commerce", _check_real, "posting"),
    ("real-performance-manager-cl.txt", "REAL · budget owner (depth inverse)", _check_budget_owner, "posting"),
    ("real-paid-media-apps-cl.txt", "REAL · adjacent (app/attribution)", _check_adjacent, "posting"),
    ("adversarial-out-of-coverage.txt", "DEGENERATE · data engineer", _check_adversarial, "posting"),
    ("goal-especialista-publicidad.txt", "GOAL · role name only", _check_goal_mode, "goal"),
]


def _render(a: dict) -> None:
    print(f"  puesto      : {a['role_title']}  [{a['seniority']}]")
    print(f"  empresa     : {a['company'] or '(no nombrada)'}")
    print(f"  cobertura   : {a['coverage']}%   ·  núcleo {a['core_lessons']} "
          f"de {a['total_lessons']} lecciones")
    print(f"  documento   : {a['doc_type']}")
    print(f"                «{a['doc_title']}»")
    print(f"  pitch       : {a['pitch']}")
    print(f"  competencias ({len(a['competencies'])}):")
    for c in a["competencies"]:
        print(f"      · {c.get('name','')}")
    print("  ruta:")
    for r in a["ruta"] or []:
        tag = "NÚCLEO " if r["phase"] == "nucleo" else "después"
        mods = ",".join(map(str, r.get("modules") or [])) or f"1..{r['through_module']}"
        print(f"      → [{tag}] {r['course_slug']} módulos [{mods}] "
              f"({r['lessons']} lecciones)")
        cov = ", ".join(f"{c['competency']} (M{c['module_no']})" for c in r["covers"])
        print(f"        cubre: {cov or '(sin respaldo de módulo)'}")
        print(f"        {r['why']}")
    if not a["ruta"]:
        print("      (vacía)")
    print("  gaps:")
    for g in a["gaps"] or []:
        print(f"      ✗ [{g.get('severity','?')}] {g.get('name','')}")
    if not a["gaps"]:
        print("      (ninguno)")


def main() -> int:
    with db.connect() as conn:
        catalog = db.job_catalog(conn)
    modules = sum(len(c["modules"]) for c in catalog)
    print(f"catálogo: {len(catalog)} cursos · {modules} módulos\n")
    if not catalog:
        print("FAIL: empty catalog — nothing to match against")
        return 1

    failed = 0
    for filename, label, check, mode in CASES:
        path = FIXTURES / filename
        print("=" * 72)
        print(label)
        print("=" * 72)
        posting = path.read_text(encoding="utf-8", errors="replace")
        analysis = writer.analyze_job_posting(posting, catalog, mode=mode)
        _render(analysis)
        problems = _invariants(analysis, catalog) + check(analysis)
        if problems:
            failed += 1
            print("\n  FAIL")
            for p in problems:
                print(f"    - {p}")
        else:
            print("\n  PASS")
        print()

    print("=" * 72)
    print(f"{len(CASES) - failed}/{len(CASES)} fixtures passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
