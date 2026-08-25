"""Bulk-upload locally rendered course videos to the cloud volume via the
admin upload endpoint. Usage:

    python upload_videos.py <course_slug>

Requires DASHBOARD_TOKEN and PUBLIC_BASE_URL (the Railway app URL) in env.
"""
import os
import sys
from pathlib import Path

import requests

STUDIO = Path(__file__).resolve().parents[1]
OUTPUT_DIR = STUDIO / "output"

slug = sys.argv[1] if len(sys.argv) > 1 else "curso-marketing-ia"
base = os.environ["PUBLIC_BASE_URL"].rstrip("/")
token = os.environ["DASHBOARD_TOKEN"]

course_dir = OUTPUT_DIR / slug
videos = sorted(course_dir.glob("*.mp4"))
print(f"uploading {len(videos)} videos for {slug} -> {base}")
failures = 0
for v in videos:
    rel = f"{slug}/{v.name}"
    # Raw streamed body (rel_path as query param): the multipart path spooled
    # through the server's ephemeral /tmp and died on files >~20MB. One retry
    # per file — transient 502s at the edge happen on big bodies.
    status = ""
    # Whole body in memory: streaming a file object from this Windows host dies
    # with WinError 10053 mid-send (observed twice); a single in-memory body is
    # how the old multipart path always transmitted reliably. ≤50MB per video,
    # so RAM is a non-issue. The SERVER still streams to disk chunk by chunk.
    body = v.read_bytes()
    for attempt in (1, 2):
        r = requests.post(
            f"{base}/api/upload-media",
            params={"token": token, "rel_path": rel},
            data=body,
            headers={"Content-Type": "application/octet-stream"},
            timeout=600,
        )
        if r.ok and r.json().get("bytes") == v.stat().st_size:
            status = "ok"
            break
        status = f"FAIL {r.status_code}" if not r.ok else \
            f"FAIL size {r.json().get('bytes')} != {v.stat().st_size}"
    if status != "ok":
        failures += 1
    print(f"  {rel}: {status}")
print(f"done — {len(videos) - failures}/{len(videos)} ok")
raise SystemExit(1 if failures else 0)
