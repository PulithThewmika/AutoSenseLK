"""
Celery task — daily chained pipeline.

Flow:  Scrape (with retry) → Snapshot → Retrain
Each step only runs after the previous one succeeds.
"""

import asyncio

from app.tasks.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(name="daily_pipeline", bind=True, max_retries=3, default_retry_delay=300)
def daily_pipeline_task(self) -> dict:
    """
    Run the full daily pipeline as a Celery task with retry.

    Uses the same chained logic as the APScheduler pipeline.
    """
    return asyncio.run(_daily_pipeline_async(self))


@celery_app.task(name="scrape_listings")
def scrape_listings_task() -> dict:
    """Run a full scrape cycle (standalone, no chaining)."""
    from app.scraper.runner import run_scrape_cycle_sync
    return run_scrape_cycle_sync()


async def _daily_pipeline_async(task_instance):
    """Async chained pipeline: Scrape → Snapshot → Retrain."""
    from app.scraper.runner import run_scrape_cycle
    from app.analytics.daily_snapshot import compute_and_save_daily_analytics
    from app.ml.trainer import train_model

    # ── Step 1: Scrape ────────────────────────────────
    logger.info("⏰ [Celery] Scrape step started")
    try:
        scrape_result = await run_scrape_cycle()
        if scrape_result.get("status") != "completed":
            raise RuntimeError(f"Scrape returned status: {scrape_result.get('status')}")
        logger.info("✅ [Celery] Scrape succeeded: %s", scrape_result)
    except Exception as exc:
        logger.error("❌ [Celery] Scrape failed, retrying: %s", exc)
        raise task_instance.retry(exc=exc)

    # ── Step 2: Snapshot (only after scrape success) ──
    logger.info("⏰ [Celery] Snapshot step started")
    try:
        snapshot_result = await compute_and_save_daily_analytics()
        logger.info("✅ [Celery] Snapshot succeeded: %s", snapshot_result)
    except Exception as exc:
        logger.error("❌ [Celery] Snapshot failed: %s", exc, exc_info=True)
        return {"status": "partial", "stage": "snapshot", "scrape": scrape_result, "error": str(exc)}

    # ── Step 3: Retrain (only after snapshot success) ─
    logger.info("⏰ [Celery] Retrain step started")
    try:
        train_model()
        logger.info("✅ [Celery] Retrain succeeded")
    except Exception as exc:
        logger.error("❌ [Celery] Retrain failed: %s", exc, exc_info=True)
        return {"status": "partial", "stage": "retrain", "scrape": scrape_result, "snapshot": snapshot_result, "error": str(exc)}

    return {"status": "completed", "scrape": scrape_result, "snapshot": snapshot_result}
