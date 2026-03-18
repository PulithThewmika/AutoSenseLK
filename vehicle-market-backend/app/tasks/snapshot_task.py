"""
Celery task — daily price snapshot archiver.
"""

import asyncio

from app.tasks.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(name="snapshot_prices")
def snapshot_prices_task() -> str:
    """Capture current prices of all active listings as daily snapshots."""
    return asyncio.run(_take_snapshots())


async def _take_snapshots() -> str:
    """Async snapshot logic — iterate listings and create PriceSnapshot docs."""
    from app.models.listing import Listing
    from app.models.price_snapshot import PriceSnapshot

    listings = await Listing.find(Listing.price > 0).to_list()
    count = 0

    for listing in listings:
        snapshot = PriceSnapshot(
            listing_id=str(listing.id),
            price=listing.price,
        )
        await snapshot.insert()
        count += 1

    logger.info("Captured %d price snapshots", count)
    return f"Price snapshots captured: {count}"
