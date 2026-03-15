"""
Ikman.lk spider — crawls vehicle listing pages and extracts ad data.
"""

import asyncio
from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.scraper.playwright_fetch import fetch_page
from app.scraper.parser import parse_listing_cards, parse_listing_detail
from app.scraper.cleaner import clean_listing


# Vehicle listing index URL template
LISTING_URL = "{base}/en/ads/sri-lanka/vehicles?page={page}"


async def crawl_listings(
    max_pages: Optional[int] = None,
    fetch_details: Optional[bool] = None,
) -> list[dict]:
    """
    Crawl ikman.lk vehicle listing pages and return cleaned listing dicts.

    1. Iterate through listing index pages (with pagination)
    2. Parse listing cards from each page
    3. Optionally fetch detail pages for richer data
    4. Clean all listings

    Args:
        max_pages: Override ``settings.SCRAPE_MAX_PAGES``
        fetch_details: Override ``settings.SCRAPE_DETAIL_PAGES``

    Returns:
        List of cleaned listing dicts ready for deduplication & storage.
    """
    if max_pages is None:
        max_pages = settings.SCRAPE_MAX_PAGES
    if fetch_details is None:
        fetch_details = settings.SCRAPE_DETAIL_PAGES

    all_listings: list[dict] = []

    # ── Step 1: Crawl listing index pages ────────────────
    for page_num in range(1, max_pages + 1):
        url = LISTING_URL.format(base=settings.SCRAPE_BASE_URL, page=page_num)
        logger.info("Crawling page %d/%d: %s", page_num, max_pages, url)

        html = await fetch_page(url)
        if not html:
            logger.warning("Failed to fetch page %d, stopping pagination", page_num)
            break

        cards = parse_listing_cards(html)
        if not cards:
            logger.info("No more listings found on page %d, stopping", page_num)
            break

        all_listings.extend(cards)
        logger.info(
            "Page %d: found %d listings (total so far: %d)",
            page_num, len(cards), len(all_listings),
        )

        # Polite delay between pages
        await asyncio.sleep(settings.SCRAPE_DELAY)

    logger.info("Total listings from index pages: %d", len(all_listings))

    # ── Step 2: Optionally fetch detail pages ────────────
    if fetch_details and all_listings:
        logger.info("Fetching detail pages for %d listings …", len(all_listings))
        all_listings = await _enrich_with_details(all_listings)

    # ── Step 3: Clean all listings ───────────────────────
    cleaned = [clean_listing(listing) for listing in all_listings]
    logger.info("Cleaned %d listings", len(cleaned))

    return cleaned


async def _enrich_with_details(listings: list[dict]) -> list[dict]:
    """
    Fetch each listing's detail page and merge additional fields
    (make, model, transmission, fuel type, etc.) into the listing dict.
    """
    enriched: list[dict] = []

    for i, listing in enumerate(listings):
        detail_url = listing.get("source_url", "")
        if not detail_url:
            enriched.append(listing)
            continue

        logger.info(
            "Fetching detail %d/%d: %s",
            i + 1, len(listings), detail_url,
        )

        html = await fetch_page(detail_url)
        if html:
            detail_data = parse_listing_detail(html)
            # Merge detail data into listing (detail takes precedence for
            # fields it provides, but don't overwrite existing non-empty values
            # with empty ones from the detail page)
            for key, value in detail_data.items():
                if value and (not listing.get(key)):
                    listing[key] = value

        enriched.append(listing)

        # Polite delay between detail page requests
        await asyncio.sleep(settings.SCRAPE_DELAY)

    return enriched
