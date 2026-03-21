"""
Scraper runner — orchestrates a full scrape cycle (segment-wise save).
1. Crawl segment by segment
2. Deduplicate against existing DB immediately
3. Store in DB immediately
4. Compute and save daily analytics
"""

import asyncio

from app.core.logging import logger
from app.scraper.ikman_spider import crawl_model, crawl_brand_no_models
from app.scraper.deduplicator import deduplicate_batch
from app.scraper.storage import save_listings
from app.analytics.daily_snapshot import compute_and_save_daily_analytics
from app.scraper.brands import BRAND_MODELS, _BRAND_ONLY, CONDITIONS, brand_display_name


async def run_scrape_cycle(
    brands: list[str] | None = None,
    conditions: list[str] | None = None,
) -> dict:
    """
    Execute the complete scrape pipeline for all brands.

    Steps:
      1. Crawl segment by segment (model-by-model or brand-level)
      2. Deduplicate and Store immediately per segment (prevents data loss)
      3. Compute daily analytics snapshot

    Returns a summary dict with statistics.
    """
    logger.info("═══ Starting full scrape cycle (Segment-wise Save) ═══")

    if conditions is None:
        conditions = CONDITIONS

    target_model_brands = list(BRAND_MODELS.keys())
    if brands:
        target_model_brands = [b for b in target_model_brands if b in brands]

    target_brand_only = _BRAND_ONLY
    if brands:
        target_brand_only = [b for b in _BRAND_ONLY if b in brands]

    total_found, total_new, total_dupes, total_saved = 0, 0, 0, 0

    async def _process_segment(listings: list[dict]):
        nonlocal total_found, total_new, total_dupes, total_saved
        if not listings:
            return
        total_found += len(listings)
        new_l, dupes = await deduplicate_batch(listings)
        total_new += len(new_l)
        total_dupes += dupes
        if new_l:
            saved = await save_listings(new_l)
            total_saved += saved

    # 1. Brands with model data
    for brand in target_model_brands:
        models = BRAND_MODELS[brand]
        make_display = brand_display_name(brand)
        logger.info("═══ %s (%d models) ═══", make_display, len(models))

        for model_display, model_slug in models:
            for condition in conditions:
                listings = await crawl_model(brand, model_display, model_slug, condition=condition)
                await _process_segment(listings)

    # 2. Brand-only brands
    for brand in target_brand_only:
        make_display = brand_display_name(brand)
        logger.info("═══ %s (brand-level) ═══", make_display)

        for condition in conditions:
            listings = await crawl_brand_no_models(brand, condition=condition)
            await _process_segment(listings)

    logger.info("═══ Finished Crawling & Saving ═══")

    if total_found == 0:
        logger.warning("No listings found — scrape cycle complete (empty)")
        return {
            "status": "completed",
            "total_found": 0,
            "new_listings": 0,
            "duplicates_skipped": 0,
            "saved": 0,
            "analytics": None,
        }

    # 4. Compute daily analytics
    analytics_summary = await compute_and_save_daily_analytics()
    logger.info("Pipeline: daily analytics computed")

    summary = {
        "status": "completed",
        "total_found": total_found,
        "new_listings": total_new,
        "duplicates_skipped": total_dupes,
        "saved": total_saved,
        "analytics": analytics_summary,
    }

    logger.info("═══ Scrape cycle complete: %s ═══", summary)
    return summary


async def run_brand_scrape(brand: str) -> dict:
    """
    Scrape a single brand across all conditions, saving segment-wise.
    """
    logger.info("═══ Starting brand scrape: %s ═══", brand)

    summary = await run_scrape_cycle(brands=[brand], conditions=CONDITIONS)
    summary["brand"] = brand
    return summary


def run_scrape_cycle_sync() -> dict:
    """Synchronous wrapper for use in Celery tasks."""
    return asyncio.run(run_scrape_cycle())
