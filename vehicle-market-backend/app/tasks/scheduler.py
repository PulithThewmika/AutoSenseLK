"""
In-process APScheduler — runs inside the FastAPI process.

Schedules:
  - scrape_listings  → daily at 00:00 (midnight) Asia/Colombo
  - snapshot_prices  → daily at 05:00 Asia/Colombo
  - retrain_model   → daily at 06:00 Asia/Colombo

This is a lightweight alternative to Celery Beat that doesn't
require a separate scheduler process or Redis.
"""

import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.logging import logger

scheduler = AsyncIOScheduler(timezone="Asia/Colombo")


async def scheduled_scrape_job():
    """Run the full scrape cycle as a scheduled job."""
    from app.scraper.runner import run_scrape_cycle

    start = datetime.now()
    logger.info("⏰ Scheduled scrape triggered at %s", start.isoformat())
    try:
        result = await run_scrape_cycle()
        elapsed = (datetime.now() - start).total_seconds()
        logger.info(
            "⏰ Scheduled scrape completed in %.1fs — found=%s new=%s saved=%s",
            elapsed,
            result.get("total_found", 0),
            result.get("new_listings", 0),
            result.get("saved", 0),
        )
    except Exception as exc:
        logger.error("⏰ Scheduled scrape FAILED: %s", exc, exc_info=True)


async def scheduled_snapshot_job():
    """Compute daily analytics snapshot as a scheduled job."""
    from app.analytics.daily_snapshot import compute_and_save_daily_analytics

    logger.info("⏰ Scheduled daily analytics snapshot triggered")
    try:
        result = await compute_and_save_daily_analytics()
        logger.info("⏰ Daily analytics complete: %s", result)
    except Exception as exc:
        logger.error("⏰ Scheduled snapshot FAILED: %s", exc, exc_info=True)


async def scheduled_retrain_job():
    """Retrain the ML model as a scheduled job."""
    from app.ml.trainer import train_model

    logger.info("⏰ Scheduled model retraining triggered")
    try:
        await asyncio.to_thread(train_model)
        logger.info("⏰ Model retraining complete")
    except Exception as exc:
        logger.error("⏰ Scheduled retrain FAILED: %s", exc, exc_info=True)


def start_scheduler():
    """Register all cron jobs and start the scheduler."""
    # ── Daily scrape at midnight ──────────────────────────
    scheduler.add_job(
        scheduled_scrape_job,
        CronTrigger(hour=0, minute=0, timezone="Asia/Colombo"),
        id="daily_scrape_midnight",
        name="Daily Scrape (midnight)",
        replace_existing=True,
        misfire_grace_time=3600,  # allow up to 1 h late
    )

    # ── Daily analytics at 5:00 AM ────────────────────────
    scheduler.add_job(
        scheduled_snapshot_job,
        CronTrigger(hour=5, minute=0, timezone="Asia/Colombo"),
        id="daily_snapshot_5am",
        name="Daily Analytics Snapshot (5 AM)",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    # ── Daily model retrain at 6:00 AM ────────────────────
    scheduler.add_job(
        scheduled_retrain_job,
        CronTrigger(hour=6, minute=0, timezone="Asia/Colombo"),
        id="daily_retrain_6am",
        name="Daily Model Retrain (6 AM)",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    scheduler.start()
    logger.info(
        "⏰ APScheduler started — next scrape at: %s",
        scheduler.get_job("daily_scrape_midnight").next_run_time,
    )


def stop_scheduler():
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("⏰ APScheduler shut down")
