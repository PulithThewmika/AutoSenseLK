"""
HTTP fetcher — uses httpx for fast requests with Playwright fallback
for JS-rendered pages.
"""

import asyncio
from typing import Optional

import httpx

from app.core.config import settings
from app.core.logging import logger

# Re-usable headers
_HEADERS = {
    "User-Agent": settings.SCRAPE_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds


async def fetch_page(url: str, *, use_playwright: bool = False) -> Optional[str]:
    """
    Fetch a page and return its HTML.

    Uses httpx by default. Falls back to Playwright if ``use_playwright``
    is True (for pages that require JS rendering).
    """
    if use_playwright:
        return await _fetch_with_playwright(url)
    return await _fetch_with_httpx(url)


async def _fetch_with_httpx(url: str) -> Optional[str]:
    """Fetch with httpx — lightweight, fast, async."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(
                headers=_HEADERS,
                follow_redirects=True,
                timeout=30.0,
            ) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                logger.debug("Fetched %s (status %d)", url, resp.status_code)
                return resp.text
        except (httpx.HTTPStatusError, httpx.RequestError) as exc:
            wait = BACKOFF_BASE ** attempt
            logger.warning(
                "Attempt %d/%d failed for %s: %s — retrying in %ds",
                attempt, MAX_RETRIES, url, exc, wait,
            )
            await asyncio.sleep(wait)

    logger.error("All %d attempts failed for %s", MAX_RETRIES, url)
    return None


async def _fetch_with_playwright(url: str) -> Optional[str]:
    """Render a JS-heavy page via Playwright and return the HTML."""
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page(user_agent=settings.SCRAPE_USER_AGENT)
            await page.goto(url, wait_until="networkidle", timeout=60_000)
            html = await page.content()
            await browser.close()
            logger.debug("Playwright fetched %s", url)
            return html
    except Exception as exc:
        logger.error("Playwright fetch failed for %s: %s", url, exc)
        return None


async def fetch_pages(urls: list[str], delay: float | None = None) -> list[str]:
    """
    Fetch multiple pages sequentially with a polite delay between requests.
    Returns list of HTML strings (skips failures).
    """
    if delay is None:
        delay = settings.SCRAPE_DELAY

    results: list[str] = []
    for url in urls:
        html = await fetch_page(url)
        if html:
            results.append(html)
        await asyncio.sleep(delay)
    return results
