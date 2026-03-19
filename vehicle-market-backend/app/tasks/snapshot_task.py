"""
Celery task — daily analytics snapshot.

Calls the daily_snapshot engine to compute and persist
PriceSnapshot aggregates and DailyAnalytics documents.
"""

import asyncio

from app.tasks.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(name="snapshot_prices")
def snapshot_prices_task() -> str:
    """Compute daily market analytics and price snapshots."""
    return asyncio.run(_run_daily_analytics())


async def _run_daily_analytics() -> str:
    """Async: compute and save all daily analytics."""
    from app.analytics.daily_snapshot import compute_and_save_daily_analytics

    result = await compute_and_save_daily_analytics()

    logger.info("Daily analytics task complete: %s", result)
    return f"Daily analytics: {result['analytics_docs_saved']} analytics, {result['price_snapshots_saved']} snapshots"
