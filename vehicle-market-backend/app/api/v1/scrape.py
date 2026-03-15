"""
Scrape API — manual trigger and status for the scraper.
"""

from fastapi import APIRouter, BackgroundTasks

from app.core.logging import logger
from app.scraper.runner import run_scrape_cycle

router = APIRouter(prefix="/scrape", tags=["scrape"])

# In-memory store for the last scrape result
_last_result: dict | None = None


async def _run_and_store():
    """Run the scrape cycle and store the result."""
    global _last_result
    try:
        _last_result = await run_scrape_cycle()
    except Exception as exc:
        logger.error("Background scrape failed: %s", exc)
        _last_result = {"status": "failed", "error": str(exc)}


@router.post("/trigger")
async def trigger_scrape(background_tasks: BackgroundTasks):
    """
    Kick off a scrape cycle in the background.

    Returns immediately with an acknowledgement.
    """
    global _last_result
    _last_result = {"status": "running"}
    background_tasks.add_task(_run_and_store)
    return {"message": "Scrape cycle started", "status": "running"}


@router.get("/status")
async def scrape_status():
    """Return the result of the last scrape run."""
    if _last_result is None:
        return {"status": "no_runs_yet"}
    return _last_result
