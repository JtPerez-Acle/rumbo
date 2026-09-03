"""Offsite export of the irreplaceable data: learner work and course content.

Videos are re-renderable; the database is not. Railway's managed Postgres has
automatic backups — this adds an operator-controlled copy OUTSIDE Railway,
per their own defense-in-depth guidance.

Usage (DATABASE_URL = the public proxy URL):
    python studio/cloud/backup_db.py            # writes backups/aprende-<utc>.json.gz
    python studio/cloud/backup_db.py --keep 14  # also prune to the newest 14 files

Restore is deliberate and manual: the export is table -> list of row dicts,
readable with any JSON tool. This is a lifeboat, not a migration system.
"""
from __future__ import annotations

import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cloud import db  # noqa: E402

# Everything that cannot be regenerated, plus what's cheap to keep alongside.
TABLES = [
    "courses", "syllabus_nodes", "module_capstones",
    "learners", "invite_codes", "progress", "submissions",
    "project_docs", "case_studies", "course_requests",
    "topics", "publish_log",
    # Added with the job-target feature (docs/08-09). job_targets had been
    # missing from this list since it shipped — anonymous analyses are demand
    # data and goal docs are learner work; both are crown jewels.
    "job_targets", "goal_docs", "waitlist",
    # Added with the features that created them, because this list has silently
    # missed a table before (the note above) and every one of these is learner
    # data or the evidence this project is short of: what a learner told us they
    # already know, what they proved with a reto, and what strangers wrote on the
    # public lesson.
    "cv_profiles", "module_exemptions", "demo_attempts",
    # Added 2026-09-03, third time this list has missed a table: it is the
    # operator worklist of people locked out and waiting. Losing it loses the
    # names of everyone who asked to be let in and never got an answer, which
    # is the most expensive row in the database at this scale.
    "access_requests",
]

# DELIBERATELY NOT BACKED UP: login_tokens and learner_sessions. Both are
# short-lived credentials; restoring them would resurrect sessions and magic
# links that the passage of time was supposed to have killed. Their absence is
# a decision, so the count below never looks like another silent omission.
EXCLUDED = ["login_tokens", "learner_sessions"]

BACKUP_DIR = Path(__file__).resolve().parents[2] / "backups"


def unlisted(conn) -> list[str]:
    """Tables the live database has that this file mentions in neither list.

    The comment above records two silent omissions and a third was found on
    2026-09-03, every time the same way: a feature shipped a table and nobody
    thought about the backup. Asking Postgres what exists is the only version of
    this check that cannot go stale, because it reads the truth rather than a
    list someone has to remember to edit.
    """
    rows = conn.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'").fetchall()
    known = set(TABLES) | set(EXCLUDED)
    return sorted(r["table_name"] for r in rows if r["table_name"] not in known)


def run(keep: int | None = None) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    BACKUP_DIR.mkdir(exist_ok=True)
    out = BACKUP_DIR / f"aprende-{stamp}.json.gz"
    export: dict[str, list] = {}
    with db.connect() as conn:
        missing = unlisted(conn)
        if missing:
            # Loud, but NOT fatal. A backup that refuses to run because the
            # schema grew is a backup you do not have on the day you need it;
            # take what we can and make the gap impossible to scroll past.
            print("!" * 68, flush=True)
            print(f"!! {len(missing)} TABLA(S) SIN RESPALDAR: {', '.join(missing)}", flush=True)
            print("!! Agregalas a TABLES (o a EXCLUDED, con la razon) en backup_db.py", flush=True)
            print("!" * 68, flush=True)
        for table in TABLES:
            rows = conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()  # noqa: S608 — fixed table list
            export[table] = rows
            print(f"  {table}: {len(rows)} rows", flush=True)
    payload = json.dumps(export, ensure_ascii=False, default=str).encode("utf-8")
    with gzip.open(out, "wb") as f:
        f.write(payload)
    print(f"backup written: {out} ({out.stat().st_size / 1024:.0f} KB)", flush=True)
    print(f"  {len(TABLES)} tablas respaldadas - {len(EXCLUDED)} excluidas a proposito "
          f"({', '.join(EXCLUDED)})", flush=True)
    if keep:
        dumps = sorted(BACKUP_DIR.glob("aprende-*.json.gz"))
        for old in dumps[:-keep]:
            old.unlink()
            print(f"  pruned: {old.name}", flush=True)
    return out


if __name__ == "__main__":
    keep_n = None
    if "--keep" in sys.argv:
        keep_n = int(sys.argv[sys.argv.index("--keep") + 1])
    run(keep=keep_n)
