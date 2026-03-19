"""
Analytics endpoints.
- GET /analytics/avg-price       — average price by make/model
- GET /analytics/trends          — price trend over time
- GET /analytics/summary         — overall market summary
- GET /analytics/depreciation    — price vs age curve
- GET /analytics/mileage         — price vs mileage curve
- GET /analytics/daily           — latest daily market snapshot
- GET /analytics/daily/history   — historical daily snapshots
- GET /analytics/daily/brand/{brand}          — daily data for a brand
- GET /analytics/daily/brand/{brand}/{cond}   — per condition
"""

from datetime import date, timedelta, datetime, timezone

from fastapi import APIRouter, Query

from app.analytics.market_summary import market_summary, avg_price_by_make_model
from app.analytics.price_trends import monthly_avg_price
from app.analytics.depreciation import depreciation_curve, mileage_curve
from app.models.daily_analytics import DailyAnalytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


# ── Existing endpoints ──────────────────────────────────

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


# ── Daily analytics endpoints ───────────────────────────

@router.get("/daily")
async def daily_latest():
    """Return the latest market-wide daily analytics snapshot."""
    doc = await DailyAnalytics.find(
        DailyAnalytics.scope == "market"
    ).sort(-DailyAnalytics.snapshot_date).first_or_none()

    if not doc:
        return {"message": "No daily analytics yet. Trigger a scrape first."}

    return _serialize_daily(doc)


@router.get("/daily/history")
async def daily_history(
    days: int = Query(30, ge=1, le=365),
    scope: str = Query("market"),
    brand: str | None = None,
):
    """Return historical daily analytics snapshots."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date()

    query: dict = {
        "scope": scope,
        "snapshot_date": {"$gte": cutoff},
    }
    if brand:
        query["brand"] = brand

    docs = await DailyAnalytics.find(query).sort(
        -DailyAnalytics.snapshot_date
    ).to_list()

    return {
        "days": days,
        "scope": scope,
        "brand": brand,
        "total": len(docs),
        "snapshots": [_serialize_daily(d) for d in docs],
    }


@router.get("/daily/brands")
async def daily_all_brands():
    """Return the latest daily snapshot for every brand."""
    # Get the most recent snapshot date
    latest = await DailyAnalytics.find(
        DailyAnalytics.scope == "brand"
    ).sort(-DailyAnalytics.snapshot_date).first_or_none()

    if not latest:
        return {"message": "No brand analytics yet.", "brands": []}

    docs = await DailyAnalytics.find(
        DailyAnalytics.scope == "brand",
        DailyAnalytics.snapshot_date == latest.snapshot_date,
    ).sort(-DailyAnalytics.total_listings).to_list()

    return {
        "date": str(latest.snapshot_date),
        "total_brands": len(docs),
        "brands": [_serialize_daily(d) for d in docs],
    }


@router.get("/daily/brand/{brand}")
async def daily_brand(brand: str):
    """Return the latest daily snapshot for a specific brand (all conditions combined)."""
    doc = await DailyAnalytics.find(
        DailyAnalytics.scope == "brand",
        DailyAnalytics.brand == brand,
    ).sort(-DailyAnalytics.snapshot_date).first_or_none()

    if not doc:
        return {"message": f"No analytics for brand '{brand}'"}

    # Also get condition breakdown
    conditions = await DailyAnalytics.find(
        DailyAnalytics.scope == "brand_condition",
        DailyAnalytics.brand == brand,
        DailyAnalytics.snapshot_date == doc.snapshot_date,
    ).to_list()

    return {
        "brand": _serialize_daily(doc),
        "conditions": [_serialize_daily(c) for c in conditions],
    }


@router.get("/daily/brand/{brand}/{condition}")
async def daily_brand_condition(brand: str, condition: str):
    """Return the latest daily snapshot for a brand + condition."""
    doc = await DailyAnalytics.find(
        DailyAnalytics.scope == "brand_condition",
        DailyAnalytics.brand == brand,
        DailyAnalytics.condition == condition,
    ).sort(-DailyAnalytics.snapshot_date).first_or_none()

    if not doc:
        return {"message": f"No analytics for {brand} [{condition}]"}

    return _serialize_daily(doc)


def _serialize_daily(doc: DailyAnalytics) -> dict:
    """Convert a DailyAnalytics document to a JSON-safe dict."""
    return {
        "date": str(doc.snapshot_date),
        "scope": doc.scope,
        "brand": doc.brand,
        "condition": doc.condition,
        "total_listings": doc.total_listings,
        "avg_price": doc.avg_price,
        "min_price": doc.min_price,
        "max_price": doc.max_price,
        "median_price": doc.median_price,
        "price_change_pct": doc.price_change_pct,
    }
