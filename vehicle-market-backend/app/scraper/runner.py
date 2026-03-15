"""
Scraper runner — orchestrates a full scrape cycle.
1. Fetch pages (ikman_spider)
2. Parse raw HTML into structured data
3. Clean & normalise values
4. Deduplicate
5. Store in DB
"""

import asyncio

from app.core.logging import logger
from app.scraper.ikman_spider import crawl_listings
from app.scraper.deduplicator import deduplicate_batch
from app.scraper.storage import save_listings


async def run_scrape_cycle() -> dict:
    """
    Execute the complete scrape pipeline.

    Returns a summary dict with statistics.
    """
    logger.info("═══ Starting scrape cycle ═══")

    # ── 1. Crawl & parse & clean ────────────────────────
    # The spider handles fetching, parsing, and cleaning internally
    listings = await crawl_listings()
    total_found = len(listings)
    logger.info("Pipeline: %d cleaned listings from spider", total_found)

    if not listings:
        logger.warning("No listings found — scrape cycle complete (empty)")
        return {
            "status": "completed",
            "total_found": 0,
            "new_listings": 0,
            "duplicates_skipped": 0,
            "saved": 0,
        }

    # ── 2. Deduplicate ──────────────────────────────────
    new_listings, duplicates_skipped = await deduplicate_batch(listings)
    logger.info(
        "Pipeline: %d new listings, %d duplicates skipped",
        len(new_listings), duplicates_skipped,
    )

    # ── 3. Store in DB ──────────────────────────────────
    saved = 0
    if new_listings:
        saved = await save_listings(new_listings)
        logger.info("Pipeline: %d listings saved to database", saved)

    summary = {
        "status": "completed",
        "total_found": total_found,
        "new_listings": len(new_listings),
        "duplicates_skipped": duplicates_skipped,
        "saved": saved,
    }

    logger.info("═══ Scrape cycle complete: %s ═══", summary)
    return summary


def run_scrape_cycle_sync() -> dict:
    """Synchronous wrapper for use in Celery tasks."""
    return asyncio.run(run_scrape_cycle())
