"""
Ikman.lk spider — crawls vehicle listing pages per brand+model and extracts ad data.

Strategy:
  - For brands WITH model data: crawl brand → model → condition (most precise)
  - For brands WITHOUT model data: crawl brand → condition (broad sweep)
"""

from __future__ import annotations

import asyncio
from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.scraper.brands import (
    BRAND_MODELS, CONDITIONS, CONDITION_URL_MAP,
    build_model_url, build_brand_url, brand_display_name,
)
from app.scraper.playwright_fetch import fetch_page
from app.scraper.parser import parse_listing_cards
from app.scraper.cleaner import clean_listing


async def crawl_model(
    brand: str,
    model_display: str,
    model_slug: str,
    condition: str | None = None,
    max_pages: int | None = None,
) -> list[dict]:
    """
    Crawl listings for a specific brand + model + condition combination.

    Returns cleaned listing dicts with make, model, and condition injected.
    """
    if max_pages is None:
        max_pages = settings.SCRAPE_MAX_PAGES_PER_BRAND

    make_display = brand_display_name(brand)
    cond_label = condition or "all"

    all_listings: list[dict] = []

    for page_num in range(1, max_pages + 1):
        url = build_model_url(brand, model_slug, condition=condition, page=page_num)

        html = await fetch_page(url)
        if not html:
            logger.warning("    ✗ %s/%s [%s] page %d — failed", make_display, model_display, cond_label, page_num)
            break

        cards = parse_listing_cards(html)
        if not cards:
            logger.info("    ✓ %s/%s [%s] page %d — no more listings", make_display, model_display, cond_label, page_num)
            break

        # Inject brand, model, condition from URL context
        for card in cards:
            card["make"] = make_display
            card["model"] = model_display
            if condition:
                card["condition"] = condition

        all_listings.extend(cards)
        await asyncio.sleep(settings.SCRAPE_DELAY)

    cleaned = [clean_listing(l) for l in all_listings]
    if cleaned:
        logger.info(
            "    ✓ %s / %s [%s]: %d listings",
            make_display, model_display, cond_label, len(cleaned),
        )
    return cleaned


async def crawl_brand_no_models(
    brand: str,
    condition: str | None = None,
    max_pages: int | None = None,
) -> list[dict]:
    """
    Crawl a brand without model-level data (brand-level URL).

    Used for brands where model registry is not yet available.
    """
    if max_pages is None:
        max_pages = settings.SCRAPE_MAX_PAGES_PER_BRAND

    make_display = brand_display_name(brand)
    cond_label = condition or "all"
    all_listings: list[dict] = []

    for page_num in range(1, max_pages + 1):
        url = build_brand_url(brand, condition=condition, page=page_num)

        html = await fetch_page(url)
        if not html:
            break

        cards = parse_listing_cards(html)
        if not cards:
            break

        for card in cards:
            card["make"] = make_display
            if condition:
                card["condition"] = condition

        all_listings.extend(cards)
        await asyncio.sleep(settings.SCRAPE_DELAY)

    cleaned = [clean_listing(l) for l in all_listings]
    if cleaned:
        logger.info("  ✓ %s [%s] (no-model): %d listings", make_display, cond_label, len(cleaned))
    return cleaned


async def crawl_all_brands(
    brands: list[str] | None = None,
    conditions: list[str] | None = None,
    max_pages: int | None = None,
) -> list[dict]:
    """
    Full market sweep — all brands × all conditions.

    For brands with model data: crawls per model × condition.
    For brands without model data: crawls per condition only.

    Returns all cleaned listings.
    """
    if conditions is None:
        conditions = CONDITIONS

    # Determine which brands to crawl
    target_model_brands = list(BRAND_MODELS.keys())
    if brands:
        target_model_brands = [b for b in target_model_brands if b in brands]

    from app.scraper.brands import _BRAND_ONLY, BRANDS
    target_brand_only = _BRAND_ONLY
    if brands:
        target_brand_only = [b for b in _BRAND_ONLY if b in brands]

    all_listings: list[dict] = []

    # ── 1. Brands with model data ─────────────────────────────────────────
    for brand in target_model_brands:
        models = BRAND_MODELS[brand]
        make_display = brand_display_name(brand)
        logger.info("═══ %s (%d models) ═══", make_display, len(models))

        for model_display, model_slug in models:
            for condition in conditions:
                listings = await crawl_model(
                    brand, model_display, model_slug,
                    condition=condition, max_pages=max_pages,
                )
                all_listings.extend(listings)

    # ── 2. Brand-only brands ──────────────────────────────────────────────
    for brand in target_brand_only:
        make_display = brand_display_name(brand)
        logger.info("═══ %s (brand-level) ═══", make_display)

        for condition in conditions:
            listings = await crawl_brand_no_models(brand, condition=condition, max_pages=max_pages)
            all_listings.extend(listings)

    logger.info("═══ Full sweep complete: %d total listings ═══", len(all_listings))
    return all_listings


async def crawl_brand(
    brand: str,
    condition: str | None = None,
    max_pages: int | None = None,
    fetch_details: bool | None = None,  # kept for compat, unused
) -> list[dict]:
    """
    Crawl a single brand across all its models (or brand-level if no models).

    Convenience wrapper used by run_brand_scrape().
    """
    if brand in BRAND_MODELS:
        all_listings: list[dict] = []
        for model_display, model_slug in BRAND_MODELS[brand]:
            listings = await crawl_model(brand, model_display, model_slug, condition=condition, max_pages=max_pages)
            all_listings.extend(listings)
        return all_listings
    else:
        return await crawl_brand_no_models(brand, condition=condition, max_pages=max_pages)


# Backward-compat alias
async def crawl_listings(
    max_pages: Optional[int] = None,
    fetch_details: Optional[bool] = None,
) -> list[dict]:
    return await crawl_all_brands(max_pages=max_pages)
