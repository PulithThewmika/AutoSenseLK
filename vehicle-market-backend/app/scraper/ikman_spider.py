"""
Ikman.lk spider — crawls vehicle listing pages per brand and extracts ad data.

Supports:
  - Per-brand crawling across all 55+ Sri Lankan vehicle brands
  - Per-condition filtering (used, brand_new, reconditioned)
  - Full market sweep: all brands × all conditions
"""

import asyncio
from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.scraper.brands import BRANDS, CONDITIONS, build_brand_url, brand_display_name
from app.scraper.playwright_fetch import fetch_page
from app.scraper.parser import parse_listing_cards, parse_listing_detail
from app.scraper.cleaner import clean_listing


async def crawl_brand(
    brand: str,
    condition: str | None = None,
    max_pages: int | None = None,
    fetch_details: bool | None = None,
) -> list[dict]:
    """
    Crawl listings for a single brand (optionally filtered by condition).

    Returns cleaned listing dicts with brand and condition injected.
    """
    if max_pages is None:
        max_pages = settings.SCRAPE_MAX_PAGES_PER_BRAND
    if fetch_details is None:
        fetch_details = settings.SCRAPE_DETAIL_PAGES

    display = brand_display_name(brand)
    cond_label = condition or "all"
    logger.info("┌─ Crawling %s [%s] (max %d pages)", display, cond_label, max_pages)

    all_listings: list[dict] = []

    for page_num in range(1, max_pages + 1):
        url = build_brand_url(brand, condition=condition, page=page_num)
        logger.info("  Page %d/%d: %s", page_num, max_pages, url)

        html = await fetch_page(url)
        if not html:
            logger.warning("  Failed to fetch page %d, stopping", page_num)
            break

        cards = parse_listing_cards(html)
        if not cards:
            logger.info("  No more listings on page %d, stopping", page_num)
            break

        # Inject brand and condition from URL context
        for card in cards:
            card.setdefault("make", brand_display_name(brand))
            if condition:
                card.setdefault("condition", condition)

        all_listings.extend(cards)
        logger.info("  Page %d: %d cards (total: %d)", page_num, len(cards), len(all_listings))

        await asyncio.sleep(settings.SCRAPE_DELAY)

    # Optionally fetch detail pages
    if fetch_details and all_listings:
        logger.info("  Fetching detail pages for %d listings …", len(all_listings))
        all_listings = await _enrich_with_details(all_listings)

    # Clean all listings
    cleaned = [clean_listing(l) for l in all_listings]
    logger.info("└─ %s [%s]: %d cleaned listings", display, cond_label, len(cleaned))

    return cleaned


async def crawl_all_brands(
    brands: list[str] | None = None,
    conditions: list[str] | None = None,
    max_pages: int | None = None,
    fetch_details: bool | None = None,
) -> list[dict]:
    """
    Crawl all brands across all conditions.

    This is the main entry point for a full market scrape.
    Iterates: each brand × each condition.
    """
    if brands is None:
        brands = BRANDS
    if conditions is None:
        conditions = CONDITIONS

    all_listings: list[dict] = []
    brand_stats: dict[str, int] = {}

    total_combos = len(brands) * len(conditions)
    current = 0

    for brand in brands:
        brand_count = 0

        for condition in conditions:
            current += 1
            logger.info(
                "═══ [%d/%d] %s × %s ═══",
                current, total_combos,
                brand_display_name(brand), condition,
            )

            listings = await crawl_brand(
                brand,
                condition=condition,
                max_pages=max_pages,
                fetch_details=fetch_details,
            )

            all_listings.extend(listings)
            brand_count += len(listings)

        brand_stats[brand] = brand_count
        logger.info("Brand %s total: %d listings", brand_display_name(brand), brand_count)

    logger.info(
        "═══ Full market crawl complete: %d brands, %d total listings ═══",
        len(brands), len(all_listings),
    )

    return all_listings


# Keep backward-compatible function name
async def crawl_listings(
    max_pages: Optional[int] = None,
    fetch_details: Optional[bool] = None,
) -> list[dict]:
    """
    Backward-compatible entry point.

    Now crawls all brands × all conditions instead of a single generic URL.
    """
    return await crawl_all_brands(
        max_pages=max_pages,
        fetch_details=fetch_details,
    )


async def _enrich_with_details(listings: list[dict]) -> list[dict]:
    """
    Fetch each listing's detail page and merge additional fields
    (model, transmission, fuel type, etc.) into the listing dict.
    """
    enriched: list[dict] = []

    for i, listing in enumerate(listings):
        detail_url = listing.get("source_url", "")
        if not detail_url:
            enriched.append(listing)
            continue

        logger.info(
            "  Detail %d/%d: %s",
            i + 1, len(listings), detail_url,
        )

        html = await fetch_page(detail_url)
        if html:
            detail_data = parse_listing_detail(html)
            for key, value in detail_data.items():
                if value and (not listing.get(key)):
                    listing[key] = value

        enriched.append(listing)
        await asyncio.sleep(settings.SCRAPE_DELAY)

    return enriched
