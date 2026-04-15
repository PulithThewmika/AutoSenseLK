"""
Scrape API — manual trigger and status for the scraper.
"""

from fastapi import APIRouter, BackgroundTasks

from app.core.logging import logger
from app.scraper.runner import run_scrape_cycle, run_brand_scrape
from app.scraper.brands import BRANDS, CONDITIONS

router = APIRouter(prefix="/scrape", tags=["scrape"])

# In-memory store for the last scrape result
_last_result: dict | None = None


async def _run_and_store(brands=None, conditions=None):
    """Run the scrape cycle and store the result."""
    global _last_result
    try:
        _last_result = await run_scrape_cycle(brands=brands, conditions=conditions)
    except Exception as exc:
        logger.error("Background scrape failed: %s", exc)
        _last_result = {"status": "failed", "error": str(exc)}


async def _run_brand_and_store(brand: str):
    """Run a single-brand scrape and store the result."""
    global _last_result
    try:
        _last_result = await run_brand_scrape(brand)
    except Exception as exc:
        logger.error("Brand scrape failed for %s: %s", brand, exc)
        _last_result = {"status": "failed", "brand": brand, "error": str(exc)}


@router.post("/trigger")
async def trigger_scrape(background_tasks: BackgroundTasks):
    """
    Kick off a full market scrape (all brands × all conditions).

    Returns immediately with an acknowledgement.
    """
    global _last_result
    _last_result = {"status": "running", "type": "full_market"}
    background_tasks.add_task(_run_and_store)
    return {
        "message": "Full market scrape started (all brands × all conditions)",
        "status": "running",
        "brands_count": len(BRANDS),
        "conditions": CONDITIONS,
    }


@router.post("/trigger/brand/{brand}")
async def trigger_brand_scrape(brand: str, background_tasks: BackgroundTasks):
    """
    Scrape a single brand across all conditions.

    Returns immediately with an acknowledgement.
    """
    global _last_result
    _last_result = {"status": "running", "type": "brand", "brand": brand}
    background_tasks.add_task(_run_brand_and_store, brand)
    return {
        "message": f"Brand scrape started for '{brand}'",
        "status": "running",
        "brand": brand,
        "conditions": CONDITIONS,
    }


@router.get("/status")
async def scrape_status():
    """Return the result of the last scrape run."""
    if _last_result is None:
        return {"status": "no_runs_yet"}
    return _last_result


@router.get("/brands")
async def list_available_brands():
    """Return the list of all supported brands and conditions."""
    return {
        "brands": BRANDS,
        "total_brands": len(BRANDS),
        "conditions": CONDITIONS,
    }


@router.get("/schedule")
async def scrape_schedule():
    """Return the current scheduler status and upcoming job times."""
    from app.tasks.scheduler import scheduler

    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        })

    return {
        "scheduler_running": scheduler.running,
        "timezone": "Asia/Colombo",
        "pipeline": "Scrape (retry ×3) → Snapshot → Retrain",
        "jobs": jobs,
    }


@router.post("/trigger/pipeline")
async def trigger_pipeline(background_tasks: BackgroundTasks):
    """
    Manually trigger the full daily pipeline:
      Scrape (with retry) → Snapshot → Retrain

    Each step only runs after the previous one succeeds.
    Returns immediately with an acknowledgement.
    """
    from app.tasks.scheduler import daily_pipeline

    global _last_result
    _last_result = {"status": "running", "type": "full_pipeline"}

    async def _run_pipeline():
        global _last_result
        _last_result = await daily_pipeline()

    background_tasks.add_task(_run_pipeline)
    return {
        "message": "Full daily pipeline started: Scrape → Snapshot → Retrain",
        "status": "running",
        "pipeline_steps": ["scrape (retry ×3)", "snapshot", "retrain"],
    }
