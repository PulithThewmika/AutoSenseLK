"""
Analytics endpoints.
- GET /analytics/avg-price   — average price by make/model
- GET /analytics/trends      — price trend over time
- GET /analytics/summary     — overall market summary
- GET /analytics/depreciation — price vs age curve
- GET /analytics/mileage     — price vs mileage curve
"""

from fastapi import APIRouter, Query

from app.analytics.market_summary import market_summary, avg_price_by_make_model
from app.analytics.price_trends import monthly_avg_price
from app.analytics.depreciation import depreciation_curve, mileage_curve

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/avg-price")
async def avg_price(
    make: str | None = None,
    model: str | None = None,
):
    """Return average price, optionally filtered by make/model."""
    return await avg_price_by_make_model(make, model)


@router.get("/trends")
async def price_trends(
    make: str | None = None,
    model: str | None = None,
    months: int = Query(12, ge=1, le=60),
):
    """Return monthly price trends."""
    trends = await monthly_avg_price(make, model, months)
    return {"make": make, "model": model, "trends": trends}


@router.get("/summary")
async def summary():
    """Return overall market statistics."""
    return await market_summary()


@router.get("/depreciation")
async def depreciation(
    make: str | None = None,
    model: str | None = None,
):
    """Return price-vs-year depreciation curve."""
    data = await depreciation_curve(make, model)
    return {"make": make, "model": model, "data": data}


@router.get("/mileage")
async def mileage(
    make: str | None = None,
    model: str | None = None,
):
    """Return price-vs-mileage curve."""
    data = await mileage_curve(make, model)
    return {"make": make, "model": model, "data": data}
