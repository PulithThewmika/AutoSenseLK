"""
Celery task — scheduled web scrape.
"""

from app.tasks.celery_app import celery_app
from app.scraper.runner import run_scrape_cycle_sync


@celery_app.task(name="scrape_listings")
def scrape_listings_task() -> dict:
    """Run a full scrape cycle as a background Celery task."""
    result = run_scrape_cycle_sync()
    return result
