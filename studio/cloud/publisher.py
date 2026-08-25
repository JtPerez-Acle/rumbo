"""Publish slot runner: for each channel assigned to the given time slot,
take the oldest APPROVED unpublished video and cross-post it via Upload-Post,
then record the result in the sidecar and the Postgres publish log.

Approve-first gate: only videos the user approved in the dashboard are
eligible. Set AUTO_APPROVE=1 to lift the gate later.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from loguru import logger

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))

from cloud import db  # noqa: E402
from generate_batch import load_channels  # noqa: E402

OUTPUT_DIR = STUDIO / "output"
UPLOAD_POST_API = "https://api.upload-post.com/api/upload"
AUTO_APPROVE = os.environ.get("AUTO_APPROVE", "0") == "1"


def _eligible_video(channel: str) -> tuple[Path, dict] | None:
    channel_dir = OUTPUT_DIR / channel
    if not channel_dir.is_dir():
        return None
    for mp4 in sorted(channel_dir.glob("*.mp4")):  # oldest first
        sidecar = mp4.with_suffix(".json")
        if not sidecar.is_file():
            continue
        meta = json.loads(sidecar.read_text(encoding="utf-8"))
        if meta.get("published"):
            continue
        if meta.get("approved") or AUTO_APPROVE:
            return mp4, meta
    return None


def _upload(video: Path, meta: dict, profile: dict, api_key: str) -> dict:
    username = profile.get("publish", {}).get("upload_post_username", "")
    platforms = profile.get("publish", {}).get("platforms", ["tiktok", "instagram", "youtube"])
    if not username:
        raise RuntimeError(f"channel {profile['slug']} has no upload_post_username configured")

    title = meta.get("title", video.stem)
    description = f"{meta.get('description', '')} {' '.join(meta.get('hashtags', []))}".strip()
    data = [
        ("user", username),
        ("title", title[:2200]),
        ("privacy_level", "PUBLIC_TO_EVERYONE"),
    ]
    for platform in platforms:
        data.append(("platform[]", platform))
    if any(p.startswith("youtube") for p in platforms):
        data += [
            ("youtube_title", title[:100]),
            ("youtube_description", description),
            ("privacyStatus", "public"),
            ("containsSyntheticMedia", "true"),
        ]

    with open(video, "rb") as f:
        response = requests.post(
            UPLOAD_POST_API,
            headers={"Authorization": f"Apikey {api_key}"},
            data=data,
            files={"video": f},
            timeout=300,
        )
    response.raise_for_status()
    return response.json()


def run_publish(slot: str) -> dict:
    """Publish for every channel whose profile publish_slot == slot (e.g. '15:00')."""
    api_key = os.environ.get("UPLOAD_POST_API_KEY", "")
    channels = load_channels()
    summary: dict = {"published": [], "skipped": [], "failed": []}

    for slug, profile in channels.items():
        if profile.get("publish", {}).get("publish_slot", "") != slot:
            continue
        found = _eligible_video(slug)
        if not found:
            logger.info(f"[{slug}] nothing approved and unpublished for slot {slot}")
            summary["skipped"].append(slug)
            continue
        video, meta = found

        if not api_key:
            logger.warning(f"[{slug}] UPLOAD_POST_API_KEY not set — would publish {video.name}")
            summary["skipped"].append(slug)
            continue

        try:
            result = _upload(video, meta, profile, api_key)
            request_id = result.get("request_id")
            import datetime as dt
            stamp = dt.datetime.now().isoformat(timespec="seconds")
            meta["published"] = {
                p: stamp for p in profile.get("publish", {}).get("platforms", [])
            }
            meta["publish_request_id"] = request_id
            video.with_suffix(".json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            if db.enabled():
                with db.connect() as conn:
                    for platform in meta["published"]:
                        db.log_publish(conn, slug, video.name, meta.get("title", ""), platform, request_id)
            summary["published"].append(f"{slug}/{video.name}")
            logger.info(f"[{slug}] published {video.name} (request {request_id})")
        except Exception as exc:
            logger.exception(f"[{slug}] publish failed: {exc}")
            summary["failed"].append(slug)

    logger.info(f"publish slot {slot} done: {summary}")
    return summary


if __name__ == "__main__":
    run_publish(sys.argv[1] if len(sys.argv) > 1 else "10:00")
