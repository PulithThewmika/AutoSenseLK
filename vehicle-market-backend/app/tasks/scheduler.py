"""
In-process APScheduler — runs inside the FastAPI process.

Daily pipeline (triggered at 00:00 Asia/Colombo):
  1. Scrape cycle   — retries up to MAX_RETRIES on failure
  2. Daily snapshot  — runs only after scrape succeeds
  3. Model retrain   — runs only after snapshot succeeds

The entire pipeline is a single chained sequence, not
independent cron jobs.
"""

import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.logging import logger

scheduler = AsyncIOScheduler(timezone="Asia/Colombo")

# ── Config ────────────────────────────────────────────
MAX_SCRAPE_RETRIES = 3          # max retry attempts for scrape
RETRY_DELAY_SECONDS = 300       # 5 minutes between retries


# ─────────────────────────────────────────────────────
#  Individual jobs
# ─────────────────────────────────────────────────────

async def _run_scrape_with_retry() -> dict:
    """
    Run the full scrape cycle with automatic retry on failure.

    Retries up to MAX_SCRAPE_RETRIES times with a delay between
    each attempt. Returns the result dict on success, raises on
    final failure.
    """
    from app.scraper.runner import run_scrape_cycle

    last_error = None

    for attempt in range(1, MAX_SCRAPE_RETRIES + 1):
        start = datetime.now()
        logger.info(
            "⏰ Scrape attempt %d/%d started at %s",
            attempt, MAX_SCRAPE_RETRIES, start.isoformat(),
        )
        try:
            result = await run_scrape_cycle()
            elapsed = (datetime.now() - start).total_seconds()

            # Check if the scrape actually produced data
            if result.get("status") == "completed":
                logger.info(
                    "✅ Scrape succeeded on attempt %d/%d in %.1fs — "
                    "found=%s new=%s saved=%s",
                    attempt, MAX_SCRAPE_RETRIES, elapsed,
                    result.get("total_found", 0),
                    result.get("new_listings", 0),
                    result.get("saved", 0),
                )
                return result

            # Unexpected status — treat as failure
            logger.warning(
                "⚠️ Scrape returned status='%s' on attempt %d/%d",
                result.get("status"), attempt, MAX_SCRAPE_RETRIES,
            )
            last_error = Exception(f"Unexpected status: {result.get('status')}")

        except Exception as exc:
            last_error = exc
            logger.error(
                "❌ Scrape attempt %d/%d FAILED: %s",
                attempt, MAX_SCRAPE_RETRIES, exc,
                exc_info=True,
            )

        # Wait before retrying (skip delay on last attempt)
        if attempt < MAX_SCRAPE_RETRIES:
            logger.info(
                "⏳ Waiting %ds before retry %d/%d …",
                RETRY_DELAY_SECONDS, attempt + 1, MAX_SCRAPE_RETRIES,
            )
            await asyncio.sleep(RETRY_DELAY_SECONDS)

    # All retries exhausted
    raise RuntimeError(
        f"Scrape failed after {MAX_SCRAPE_RETRIES} attempts. "
        f"Last error: {last_error}"
    )


async def _run_snapshot() -> dict:
    """Compute daily analytics snapshot."""
    from app.analytics.daily_snapshot import compute_and_save_daily_analytics

    logger.info("⏰ Daily analytics snapshot started")
    result = await compute_and_save_daily_analytics()
    logger.info("✅ Daily analytics snapshot complete: %s", result)
    return result


async def _run_retrain():
    """Retrain the ML model."""
    from app.ml.trainer import train_model

    logger.info("⏰ Model retraining started")
    await asyncio.to_thread(train_model)
    logger.info("✅ Model retraining complete")


# ─────────────────────────────────────────────────────
#  Chained daily pipeline
# ─────────────────────────────────────────────────────

async def daily_pipeline():
    """
    Full daily pipeline — runs as one chained job at midnight.

    Flow:
      Scrape (with retry) → Snapshot → Retrain
      Each step only runs if the previous one succeeded.
    """
    pipeline_start = datetime.now()
    logger.info("═══════════════════════════════════════════════")
    logger.info("⏰ DAILY PIPELINE STARTED at %s", pipeline_start.isoformat())
    logger.info("═══════════════════════════════════════════════")

    # ── Step 1: Scrape (with retry) ───────────────────
    try:
        scrape_result = await _run_scrape_with_retry()
    except RuntimeError as exc:
        logger.error(
            "🛑 DAILY PIPELINE ABORTED — scrape failed after all retries: %s",
            exc,
        )
        return {
            "status": "failed",
            "stage": "scrape",
            "error": str(exc),
        }

    # ── Step 2: Daily snapshot (only if scrape succeeded) ─
    try:
        snapshot_result = await _run_snapshot()
    except Exception as exc:
        logger.error(
            "🛑 DAILY PIPELINE — snapshot failed (scrape was OK): %s",
            exc, exc_info=True,
        )
        return {
            "status": "partial",
            "stage": "snapshot",
            "scrape": scrape_result,
            "error": str(exc),
        }

    # ── Step 3: Model retrain (only if snapshot succeeded) ─
    try:
        await _run_retrain()
    except Exception as exc:
        logger.error(
            "🛑 DAILY PIPELINE — retrain failed (scrape+snapshot OK): %s",
            exc, exc_info=True,
        )
        return {
            "status": "partial",
            "stage": "retrain",
            "scrape": scrape_result,
            "snapshot": snapshot_result,
            "error": str(exc),
        }

    elapsed = (datetime.now() - pipeline_start).total_seconds()
    logger.info("═══════════════════════════════════════════════")
    logger.info("✅ DAILY PIPELINE COMPLETE in %.1fs", elapsed)
    logger.info("═══════════════════════════════════════════════")

    return {
        "status": "completed",
        "elapsed_seconds": round(elapsed, 1),
        "scrape": scrape_result,
        "snapshot": snapshot_result,
    }


# ─────────────────────────────────────────────────────
#  Scheduler lifecycle
# ─────────────────────────────────────────────────────

def start_scheduler():
    """Register the daily pipeline and start the scheduler."""
    scheduler.add_job(
        daily_pipeline,
        CronTrigger(hour=0, minute=0, timezone="Asia/Colombo"),
        id="daily_pipeline_midnight",
        name="Daily Pipeline (Scrape → Snapshot → Retrain)",
        replace_existing=True,
        misfire_grace_time=3600,  # allow up to 1 h late if server was down
    )

    scheduler.start()

    job = scheduler.get_job("daily_pipeline_midnight")
    logger.info(
        "⏰ APScheduler started — next pipeline run at: %s",
        job.next_run_time if job else "N/A",
    )


def stop_scheduler():
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("⏰ APScheduler shut down")
