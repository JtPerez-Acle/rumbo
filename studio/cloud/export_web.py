"""Export the public catalog to files the frontend build can read.

WHY THIS EXISTS. The public pages are generated at build time (Astro, static),
and the build runs inside a Docker stage with no database and no network. So
the data those pages are about — fourteen courses, seventy modules, four hundred
and twenty lesson titles — has to ship as files in the repo.

WHAT IT COSTS, stated plainly: a new course goes live on the next deploy, not on
the database write that creates it. Courses arrive roughly monthly and already
need a deploy for their videos, so the cost is close to zero — but it is a real
change in how the catalog updates and it should never be discovered by surprise.
`course_factory <slug> all` ends by telling you to run this.

WHAT IT MUST NOT DO: invent, reshape or filter. Every payload here comes from
the same endpoint function the browser calls, so a page built from these files
and a page hydrated from the API can never describe a different catalog. That
is the whole discipline — this file is a serializer, not a second source of
truth.

    python studio/cloud/export_web.py            # write the files
    python studio/cloud/export_web.py --check    # exit 1 if they are stale

`--check` is the one that matters in a deploy: it re-exports into memory and
diffs. A stale export is silent — the site simply keeps showing last month's
catalog — so the staleness has to be made loud somewhere.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "studio" / "web" / "src" / "data"

sys.path.insert(0, str(REPO / "studio" / "dashboard"))


def collect() -> dict[str, object]:
    """Every payload the public build needs, keyed by its filename.

    Imported inside the function: this module is imported by the check runner
    and by course_factory, and neither should pay for a database driver it may
    not use.
    """
    import learn_routes

    catalog = learn_routes.public_catalog()
    files: dict[str, object] = {"catalog.json": catalog}

    # One file per course rather than one large map. Astro's getStaticPaths
    # reads the catalog to know WHICH pages exist and each course file to fill
    # one in, so a change to a single temario touches a single file — which is
    # what makes the diff on a course rewrite readable.
    for course in catalog.get("courses", []):
        slug = course["slug"]
        files[f"courses/{slug}.json"] = learn_routes.public_course(slug)

    # The free lesson on the landing. It is a real lesson from a real course,
    # chosen by the same query the SPA's /public/demo uses.
    files["demo.json"] = learn_routes.demo_payload()

    # Three numbers, in their own file on purpose.
    #
    # The landing said "70 módulos en 14 cursos" and the analyser's progress
    # copy said "las 210 lecciones" — hardcoded, and by 2026-09-03 wrong by a
    # course and by half the catalog respectively. The analyser one is the worse
    # sin: that component's own comment says a progress display that lies is
    # worse than none.
    #
    # Separate from catalog.json because `route.js` runs in the browser. Reading
    # the totals off the full catalog there would ship every course title and
    # description into the job-analyser bundle to render two integers.
    #
    # Counted over exactly the courses the catalog page lists, so every public
    # number agrees with every other one — that agreement is the whole point,
    # and it is worth more than a subtler definition that makes /cursos and the
    # landing disagree the first time a course renders no video.
    courses_out = catalog.get("courses", [])
    files["totals.json"] = {
        "courses": len(courses_out),
        "modules": sum(c["modules"] for c in courses_out),
        "lessons": sum(c["total"] for c in courses_out),
    }
    return files


def _serialize(payload: object) -> str:
    """Stable bytes for the same data.

    sort_keys is not cosmetic: without it a re-export reorders dict keys on
    nothing but a Python upgrade, every file shows as changed, and `--check`
    becomes a source of noise people learn to ignore.
    """
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write(files: dict[str, object]) -> list[str]:
    written = []
    for name, payload in files.items():
        path = OUT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_serialize(payload), encoding="utf-8")
        written.append(name)
    return written


def check(files: dict[str, object]) -> list[str]:
    """Names that are missing or differ from what the database says now."""
    stale = []
    for name, payload in files.items():
        path = OUT / name
        if not path.exists():
            stale.append(f"{name} (missing)")
        elif path.read_text(encoding="utf-8") != _serialize(payload):
            stale.append(f"{name} (differs)")
    # A course DELETED from the database leaves its file behind, and a page for
    # a course that no longer exists is worse than a missing one.
    known = {n for n in files if n.startswith("courses/")}
    for path in sorted((OUT / "courses").glob("*.json")) if (OUT / "courses").exists() else []:
        if f"courses/{path.name}" not in known:
            stale.append(f"courses/{path.name} (orphan — course is gone)")
    return stale


def main() -> int:
    files = collect()
    courses = len(files.get("catalog.json", {}).get("courses", []))  # type: ignore[union-attr]
    if courses == 0:
        # Empty is never right, and an empty export would silently ship a site
        # with no catalog at all. Fail instead.
        print("export-web: the catalog came back empty — refusing to write",
              file=sys.stderr)
        return 1

    if "--check" in sys.argv:
        stale = check(files)
        if stale:
            print(f"export-web: {len(stale)} file(s) out of date:", file=sys.stderr)
            for name in stale:
                print(f"  {name}", file=sys.stderr)
            print("\n  fix: python studio/cloud/export_web.py", file=sys.stderr)
            return 1
        print(f"export-web: up to date ({courses} courses)")
        return 0

    written = write(files)
    print(f"export-web: wrote {len(written)} files ({courses} courses) to "
          f"{OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
