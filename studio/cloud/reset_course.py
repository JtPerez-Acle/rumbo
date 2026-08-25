"""Reset ONE course to draft so its scripts regenerate under the current voice guide.

Clears that course's node scripts/quizzes/videos, its pending queue entries and
its rendered outputs. The syllabus itself (titles, objectives, modules) is kept —
to regenerate the structure too, delete the course's syllabus_nodes rows first.

Usage: python reset_course.py <course_slug> [--force]

Destructive, so it refuses to run when the course has learner data unless you
pass --force. It also prints what it is about to remove and requires the slug to
exist: the previous version defaulted to curso-marketing-ia when called with no
argument, which is a live course.
"""
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))
from cloud import db  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
force = "--force" in sys.argv
if not args:
    sys.exit("usage: python reset_course.py <course_slug> [--force]")
SLUG = args[0]

with db.connect() as conn:
    course = conn.execute("SELECT * FROM courses WHERE slug=%s", (SLUG,)).fetchone()
    if not course:
        sys.exit(f"no existe el curso {SLUG!r}")
    # Never silently destroy work a learner did. Progress and submissions both
    # hang off syllabus_nodes, and video_file=NULL would strand their lessons.
    counts = conn.execute(
        "SELECT (SELECT COUNT(*) FROM progress p JOIN syllabus_nodes n ON n.id = p.node_id "
        "        WHERE n.course_id = %(cid)s) AS progreso, "
        "       (SELECT COUNT(*) FROM submissions s JOIN syllabus_nodes n ON n.id = s.node_id "
        "        WHERE n.course_id = %(cid)s) AS entregas",
        {"cid": course["id"]},
    ).fetchone()
    if (counts["progreso"] or counts["entregas"]) and not force:
        sys.exit(f"{SLUG} tiene datos de alumnos "
                 f"({counts['progreso']} progreso, {counts['entregas']} entregas). "
                 f"Usa --force solo si estás seguro.")
    n = conn.execute(
        "UPDATE syllabus_nodes SET status='draft', quiz=NULL, video_file=NULL "
        "WHERE course_id=%s", (course["id"],)).rowcount
    conn.commit()
    print(f"reset {SLUG}: {n} nodos a draft")

# Only THIS course's queue entries. The old glob was "curso-*.json", which
# matched every course (they are all named curso-*) and wiped a concurrent
# render queue. Queue files are now namespaced <course-slug>-<pos>-<slug>.json;
# the legacy pattern is handled by reading the channel field.
pending = STUDIO / "queue" / "pending"
removed = 0
if pending.is_dir():
    import json
    for p in pending.glob("*.json"):
        try:
            if json.loads(p.read_text(encoding="utf-8")).get("channel") != SLUG:
                continue
        except (ValueError, OSError):
            continue          # unreadable entry: leave it alone rather than guess
        p.unlink()
        removed += 1

outdir = STUDIO / "output" / SLUG
files = 0
if outdir.is_dir():
    for f in outdir.iterdir():
        if f.is_file():
            f.unlink()
            files += 1
print(f"cola: {removed} entradas eliminadas · salidas: {files} archivos eliminados")
