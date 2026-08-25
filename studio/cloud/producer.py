"""Daily production run: for each channel, pick (or generate) a fresh topic,
have Claude write the script, render the video through the existing batch
runner, and record the topic as used.

Rendering reuses studio/generate_batch.py end to end: the producer writes a
queue JSON and invokes the runner, so cloud production and manual production
share one code path.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from loguru import logger

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))

from cloud import db, writer  # noqa: E402
from generate_batch import load_channels  # noqa: E402

PENDING_DIR = STUDIO / "queue" / "pending"
OUTPUT_DIR = STUDIO / "output"
BUFFER_MAX = int(os.environ.get("BUFFER_MAX", "5"))
MIN_BACKLOG = int(os.environ.get("MIN_BACKLOG", "3"))
IDEATE_AMOUNT = int(os.environ.get("IDEATE_AMOUNT", "15"))


def _unpublished_count(channel: str) -> int:
    channel_dir = OUTPUT_DIR / channel
    if not channel_dir.is_dir():
        return 0
    count = 0
    for sidecar in channel_dir.glob("*.json"):
        try:
            meta = json.loads(sidecar.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not meta.get("published"):
            count += 1
    return count


def _safe_slug(slug: str) -> str:
    slug = re.sub(r"[^a-z0-9-]", "", slug.lower().replace(" ", "-"))
    return slug[:60] or "tema"


def _queue_entry(channel: str, spec: dict) -> Path:
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    path = PENDING_DIR / f"{_safe_slug(spec['slug'])}.json"
    entry = {
        "channel": channel,
        "subject": spec["subject"],
        "title": spec["title"],
        "description": spec["description"],
        "hashtags": spec["hashtags"],
        "script": spec["script"],
        "terms": spec["terms"],
    }
    path.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def run_produce() -> dict:
    """Produce one video per channel (respecting the buffer cap). Returns a summary."""
    if not db.enabled():
        raise RuntimeError("DATABASE_URL not set — producer requires Postgres")
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise RuntimeError("OPENROUTER_API_KEY not set — producer cannot write scripts")

    channels = load_channels()
    summary: dict = {"produced": [], "skipped": [], "failed": []}
    queued_channels: list[str] = []

    with db.connect() as conn:
        for slug, profile in channels.items():
            if profile.get("kind") == "course":
                continue  # course profiles render via course_factory, never the daily producer
            buffered = _unpublished_count(slug)
            if buffered >= BUFFER_MAX:
                logger.info(f"[{slug}] buffer full ({buffered} unpublished), skipping")
                summary["skipped"].append(slug)
                continue

            try:
                backlog = db.unused_topics(conn, slug)
                is_news = bool(profile.get("use_web_search")) or slug == "ia-al-dia"
                # News runs fresh every day; evergreen channels draw from the backlog.
                if not is_news and len(backlog) < MIN_BACKLOG:
                    history = db.topic_history(conn, slug)
                    ideas = writer.ideate(profile, history, IDEATE_AMOUNT)
                    added = db.add_topics(conn, slug, ideas)
                    conn.commit()
                    logger.info(f"[{slug}] ideated {added} new topics")
                    backlog = db.unused_topics(conn, slug)

                if is_news:
                    history = db.topic_history(conn, slug)
                    ideas = writer.ideate(profile, history, 3)
                    db.add_topics(conn, slug, ideas)
                    conn.commit()
                    backlog = db.unused_topics(conn, slug)

                if not backlog:
                    logger.warning(f"[{slug}] no topics available")
                    summary["failed"].append(slug)
                    continue

                topic = backlog[0]
                spec = writer.write_video(profile, topic, use_web_search=is_news)
                spec["slug"] = topic["slug"]
                _queue_entry(slug, spec)
                db.mark_topic_used(conn, topic["id"])
                conn.commit()
                queued_channels.append(slug)
                logger.info(f"[{slug}] scripted: {spec['title']}")
            except Exception as exc:
                logger.exception(f"[{slug}] production failed: {exc}")
                summary["failed"].append(slug)

    # Render everything queued in one batch (sequential; ffmpeg is CPU-bound).
    if queued_channels:
        result = subprocess.run(
            [sys.executable, str(STUDIO / "generate_batch.py")],
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode != 0:
            logger.error("batch render reported failures")
        summary["produced"] = queued_channels

    logger.info(f"produce run done: {summary}")
    return summary


if __name__ == "__main__":
    run_produce()
