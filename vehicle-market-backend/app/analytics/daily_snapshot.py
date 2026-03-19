"""
Daily analytics snapshot engine.

Computes and persists daily market analytics at three levels:
  1. Market-wide   → 1 document per day
  2. Per-brand     → 55+ documents per day
  3. Per-brand × condition → ~165 documents per day
"""

from datetime import date, datetime, timedelta, timezone
from typing import Optional

from app.core.logging import logger
from app.models.listing import Listing
from app.models.daily_analytics import DailyAnalytics


async def compute_and_save_daily_analytics(
    snapshot_date: date | None = None,
) -> dict:
    """
    Compute and persist daily analytics for the entire market.

    Returns a summary of what was computed.
    """
    if snapshot_date is None:
        snapshot_date = datetime.now(timezone.utc).date()

    logger.info("═══ Computing daily analytics for %s ═══", snapshot_date)

    # Delete existing snapshots for this date (idempotent re-runs)
    await DailyAnalytics.find(
        DailyAnalytics.snapshot_date == snapshot_date
    ).delete()

    saved = 0

    # ── 1. Market-wide snapshot ──────────────────────────
    market = await _compute_scope(snapshot_date, scope="market")
    if market:
        await market.insert()
        saved += 1
        logger.info("Market-wide: %d listings, avg Rs. %s", market.total_listings, f"{market.avg_price:,.0f}")

    # ── 2. Per-brand snapshots ───────────────────────────
    brands = await Listing.distinct("make_id")
    brands = [b for b in brands if b]

    for brand in brands:
        doc = await _compute_scope(snapshot_date, scope="brand", brand=brand)
        if doc and doc.total_listings > 0:
            await doc.insert()
            saved += 1

    logger.info("Per-brand snapshots: %d brands", len(brands))

    # ── 3. Per-brand × condition snapshots ───────────────
    conditions = await Listing.distinct("condition")
    conditions = [c for c in conditions if c]

    for brand in brands:
        for condition in conditions:
            doc = await _compute_scope(
                snapshot_date, scope="brand_condition",
                brand=brand, condition=condition,
            )
            if doc and doc.total_listings > 0:
                await doc.insert()
                saved += 1

    logger.info("═══ Daily analytics complete: %d snapshots saved ═══", saved)

    return {
        "date": str(snapshot_date),
        "snapshots_saved": saved,
        "brands_covered": len(brands),
        "conditions_covered": len(conditions),
    }


async def _compute_scope(
    snapshot_date: date,
    scope: str,
    brand: str | None = None,
    condition: str | None = None,
) -> Optional[DailyAnalytics]:
    """Compute analytics for a specific scope (market / brand / brand_condition)."""

    # Build match filter
    match_stage: dict = {"price": {"$gt": 0}}
    if brand:
        match_stage["make_id"] = brand
    if condition:
        match_stage["condition"] = condition

    # Aggregation pipeline
    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": None,
                "total": {"$sum": 1},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "prices": {"$push": "$price"},
            }
        },
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    if not results:
        return None

    r = results[0]
    prices = sorted(r["prices"])
    n = len(prices)
    median = prices[n // 2] if n % 2 == 1 else (prices[n // 2 - 1] + prices[n // 2]) / 2

    # Compute change vs previous day
    price_change_pct = await _compute_change(
        snapshot_date, scope, brand, condition, r["avg_price"]
    )

    return DailyAnalytics(
        snapshot_date=snapshot_date,
        scope=scope,
        brand=brand,
        condition=condition,
        total_listings=r["total"],
        avg_price=round(r["avg_price"], 2),
        min_price=round(r["min_price"], 2),
        max_price=round(r["max_price"], 2),
        median_price=round(median, 2),
        price_change_pct=price_change_pct,
    )


async def _compute_change(
    current_date: date,
    scope: str,
    brand: str | None,
    condition: str | None,
    current_avg: float,
) -> Optional[float]:
    """Compare current avg price to the previous day's snapshot."""
    yesterday = current_date - timedelta(days=1)

    query = {
        "snapshot_date": yesterday,
        "scope": scope,
    }
    if brand:
        query["brand"] = brand
    if condition:
        query["condition"] = condition

    prev = await DailyAnalytics.find_one(query)

    if not prev or prev.avg_price == 0:
        return None

    change = ((current_avg - prev.avg_price) / prev.avg_price) * 100
    return round(change, 2)
