"""
Scraper runner — orchestrates a full scrape cycle.
1. Crawl all brands × conditions (ikman_spider)
2. Deduplicate against existing DB
3. Store in DB
4. Compute and save daily analytics
"""

import asyncio

from app.core.logging import logger
from app.scraper.ikman_spider import crawl_all_brands, crawl_brand
from app.scraper.deduplicator import deduplicate_batch
from app.scraper.storage import save_listings
from app.analytics.daily_snapshot import compute_and_save_daily_analytics


async def run_scrape_cycle(
    brands: list[str] | None = None,
    conditions: list[str] | None = None,
) -> dict:
    """
    Execute the complete scrape pipeline for all brands.

    Steps:
      1. Crawl all brands × all conditions
      2. Deduplicate
      3. Store new listings
      4. Compute daily analytics snapshot

    Returns a summary dict with statistics.
    """
    logger.info("═══ Starting full scrape cycle ═══")

    # ── 1. Crawl ─────────────────────────────────────────
    listings = await crawl_all_brands(brands=brands, conditions=conditions)
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
            "analytics": None,
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

    # ── 4. Compute daily analytics ──────────────────────
    analytics_summary = await compute_and_save_daily_analytics()
    logger.info("Pipeline: daily analytics computed")

    summary = {
        "status": "completed",
        "total_found": total_found,
        "new_listings": len(new_listings),
        "duplicates_skipped": duplicates_skipped,
        "saved": saved,
        "analytics": analytics_summary,
    }

    logger.info("═══ Scrape cycle complete: %s ═══", summary)
    return summary


async def run_brand_scrape(brand: str) -> dict:
    """
    Scrape a single brand across all conditions.

    Useful for on-demand brand-specific scraping.
    """
    logger.info("═══ Starting brand scrape: %s ═══", brand)

    from app.scraper.brands import CONDITIONS

    all_listings: list[dict] = []
    for condition in CONDITIONS:
        listings = await crawl_brand(brand, condition=condition)
        all_listings.extend(listings)

    if not all_listings:
        return {"status": "completed", "brand": brand, "total_found": 0, "saved": 0}

    new_listings, duplicates_skipped = await deduplicate_batch(all_listings)

    saved = 0
    if new_listings:
        saved = await save_listings(new_listings)

    return {
        "status": "completed",
        "brand": brand,
        "total_found": len(all_listings),
        "new_listings": len(new_listings),
        "duplicates_skipped": duplicates_skipped,
        "saved": saved,
    }


def run_scrape_cycle_sync() -> dict:
    """Synchronous wrapper for use in Celery tasks."""
    return asyncio.run(run_scrape_cycle())
