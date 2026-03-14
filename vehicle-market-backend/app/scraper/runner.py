"""
Scraper runner — orchestrates a full scrape cycle.
1. Fetch pages (ikman_spider / playwright_fetch)
2. Parse raw HTML into structured data
3. Clean & normalise values
4. Deduplicate
5. Store in DB
"""

from app.core.logging import logger


def run_scrape_cycle() -> None:
    """Execute the complete scrape pipeline."""
    logger.info("Starting scrape cycle …")
    # TODO: wire up spider → parser → cleaner → deduplicator → storage
    logger.info("Scrape cycle complete.")
