"""APScheduler wiring: one daily production run plus the three publish slots.

Runs inside the dashboard process (single Railway service = shared volume for
renders, dashboard, and publishing). Times are local to SCHEDULE_TZ.
"""
from __future__ import annotations

import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from cloud.producer import run_produce
from cloud.publisher import run_publish

PUBLISH_SLOTS = ["12:00", "19:00", "21:00"]
PRODUCE_AT = os.environ.get("PRODUCE_AT", "06:00")
TZ = os.environ.get("SCHEDULE_TZ", "America/Santiago")


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone=TZ)

    hour, minute = PRODUCE_AT.split(":")
    scheduler.add_job(
        _safe(run_produce), CronTrigger(hour=int(hour), minute=int(minute), timezone=TZ),
        id="produce", name="Producción diaria",
        misfire_grace_time=3600, coalesce=True,
    )
    for slot in PUBLISH_SLOTS:
        hour, minute = slot.split(":")
        scheduler.add_job(
            _safe(run_publish, slot), CronTrigger(hour=int(hour), minute=int(minute), timezone=TZ),
            id=f"publish-{slot}", name=f"Publicación {slot}",
            misfire_grace_time=1800, coalesce=True,
        )

    scheduler.start()
    logger.info(f"scheduler started (tz={TZ}, produce={PRODUCE_AT}, publish={PUBLISH_SLOTS})")
    return scheduler


def _safe(fn, *args):
    def wrapped():
        try:
            fn(*args)
        except Exception as exc:
            logger.exception(f"scheduled job {fn.__name__}{args} failed: {exc}")
    wrapped.__name__ = fn.__name__
    return wrapped
