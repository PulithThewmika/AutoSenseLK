"""
Analytics endpoints.
- GET /analytics/avg-price   — average price by make/model
- GET /analytics/trends      — price trend over time
"""

from fastapi import APIRouter, Query

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/avg-price")
async def avg_price(
    make: str | None = None,
    model: str | None = None,
):
    """Return average price, optionally filtered by make/model."""
    # TODO: aggregate from DB
    return {"avg_price": 0.0}


@router.get("/trends")
async def price_trends(
    make: str | None = None,
    model: str | None = None,
    months: int = Query(12, ge=1, le=60),
):
    """Return monthly price trends."""
    # TODO: compute from price_snapshots
    return {"months": months, "trends": []}
