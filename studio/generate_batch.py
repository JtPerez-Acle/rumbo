"""Batch renderer for the 4-channel Spanish AI shorts studio.

Reads channel profiles from channels/*.toml and pending video specs from
queue/pending/*.json, renders each one through the MoneyPrinterTurbo CLI,
then moves results to output/<channel>/ and the spec to queue/done/.

Usage:
    python generate_batch.py                 # render everything pending
    python generate_batch.py --channel codigo-ia
    python generate_batch.py --dry-run       # show what would render
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tomllib
import uuid
from pathlib import Path

STUDIO = Path(__file__).resolve().parent
REPO = STUDIO.parent / "MoneyPrinterTurbo"
VENV_PYTHON = REPO / ".venv" / "Scripts" / "python.exe"
PENDING_DIR = STUDIO / "queue" / "pending"
DONE_DIR = STUDIO / "queue" / "done"
OUTPUT_DIR = STUDIO / "output"


def load_channels() -> dict[str, dict]:
    channels = {}
    for path in (STUDIO / "channels").glob("*.toml"):
        with open(path, "rb") as f:
            profile = tomllib.load(f)
        channels[profile["slug"]] = profile
    return channels


def build_cli_args(entry: dict, profile: dict, task_id: str) -> list[str]:
    voice = profile["voice"]
    style = profile["style"]
    args = [
        str(VENV_PYTHON), "cli.py",
        "--task-id", task_id,
        "--video-subject", entry["subject"],
        "--video-script", entry["script"],
        "--video-terms", entry["terms"],
        "--video-language", "es",
        "--voice-name", voice["voice_name"],
        "--voice-rate", str(voice.get("voice_rate", 1.0)),
        "--font-name", style["font_name"],
        "--font-size", str(style["font_size"]),
        "--text-fore-color", style["text_fore_color"],
        "--stroke-color", style["stroke_color"],
        "--stroke-width", str(style["stroke_width"]),
        "--video-aspect", style.get("video_aspect", "9:16"),
        "--video-clip-duration", str(style.get("video_clip_duration", 4)),
        "--bgm-volume", str(style.get("bgm_volume", 0.15)),
    ]
    if style.get("video_transition_mode"):
        args += ["--video-transition-mode", style["video_transition_mode"]]
    if style.get("subtitle_position"):
        args += ["--subtitle-position", style["subtitle_position"]]
        if style["subtitle_position"] == "custom":
            args += ["--custom-position", str(style.get("custom_position", 70))]
    return args


def render_entry(entry_path: Path, entry: dict, profile: dict) -> Path | None:
    task_id = str(uuid.uuid4())
    args = build_cli_args(entry, profile, task_id)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    print(f"[{profile['slug']}] rendering: {entry['subject']} (task {task_id})")
    result = subprocess.run(
        args, cwd=REPO, env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    video = REPO / "storage" / "tasks" / task_id / "final-1.mp4"
    if result.returncode != 0 or not video.is_file():
        print(f"[{profile['slug']}] FAILED: {entry['subject']} "
              f"(exit {result.returncode}, log: storage/tasks/{task_id})")
        return None

    today = dt.date.today().isoformat()
    slug = entry_path.stem
    channel_dir = OUTPUT_DIR / profile["slug"]
    channel_dir.mkdir(parents=True, exist_ok=True)
    dest_video = channel_dir / f"{today}-{slug}.mp4"
    shutil.copy2(video, dest_video)

    metadata = {
        "channel": profile["slug"],
        "date": today,
        "task_id": task_id,
        "video": dest_video.name,
        "subject": entry["subject"],
        "title": entry.get("title", entry["subject"]),
        "description": entry.get("description", ""),
        "hashtags": entry.get("hashtags", []),
    }
    dest_video.with_suffix(".json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    DONE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(entry_path, DONE_DIR / f"{today}-{entry_path.name}")
    print(f"[{profile['slug']}] done -> {dest_video}")
    return dest_video


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", help="only render entries for this channel slug")
    parser.add_argument("--dry-run", action="store_true", help="list pending work and exit")
    opts = parser.parse_args()

    channels = load_channels()
    pending = sorted(PENDING_DIR.glob("*.json")) if PENDING_DIR.is_dir() else []
    entries = []
    for path in pending:
        entry = json.loads(path.read_text(encoding="utf-8"))
        if entry["channel"] not in channels:
            print(f"skip {path.name}: unknown channel {entry['channel']!r}")
            continue
        if opts.channel and entry["channel"] != opts.channel:
            continue
        entries.append((path, entry))

    if not entries:
        print("nothing pending.")
        return 0
    if opts.dry_run:
        for path, entry in entries:
            print(f"[{entry['channel']}] {path.name}: {entry['subject']}")
        return 0

    failures = 0
    for path, entry in entries:
        if render_entry(path, entry, channels[entry["channel"]]) is None:
            failures += 1

    print(f"batch finished: {len(entries) - failures}/{len(entries)} ok")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
