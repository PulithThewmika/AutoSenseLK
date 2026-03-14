"""
Celery task — scheduled web scrape.
"""

from app.tasks.celery_app import celery_app
from app.scraper.runner import run_scrape_cycle


@celery_app.task(name="scrape_listings")
def scrape_listings_task() -> str:
    """Run a full scrape cycle as a background Celery task."""
    run_scrape_cycle()
    return "Scrape cycle completed"
