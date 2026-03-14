"""
Celery task — daily price snapshot archiver.
"""

from app.tasks.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(name="snapshot_prices")
def snapshot_prices_task() -> str:
    """Capture current prices of all active listings as daily snapshots."""
    logger.info("Taking daily price snapshots …")
    # TODO: iterate listings and insert into price_snapshots table
    return "Price snapshots captured"
