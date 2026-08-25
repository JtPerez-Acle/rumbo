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
]

BACKUP_DIR = Path(__file__).resolve().parents[2] / "backups"


def run(keep: int | None = None) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    BACKUP_DIR.mkdir(exist_ok=True)
    out = BACKUP_DIR / f"aprende-{stamp}.json.gz"
    export: dict[str, list] = {}
    with db.connect() as conn:
        for table in TABLES:
            rows = conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()  # noqa: S608 — fixed table list
            export[table] = rows
            print(f"  {table}: {len(rows)} rows", flush=True)
    payload = json.dumps(export, ensure_ascii=False, default=str).encode("utf-8")
    with gzip.open(out, "wb") as f:
        f.write(payload)
    print(f"backup written: {out} ({out.stat().st_size / 1024:.0f} KB)", flush=True)
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
