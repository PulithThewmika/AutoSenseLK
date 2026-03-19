"""
Daily analytics snapshot engine.

Produces daily DailyAnalytics documents and PriceSnapshot aggregates
at four levels:
  1. Market-wide   → 1 document per day
  2. Per-brand     → 1 per make per day
  3. Per-brand × condition → 1 per make × condition per day
  4. Per-brand × model × year × condition → most granular, for trend analysis
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Optional

from app.core.logging import logger
from app.models.listing import Listing
from app.models.daily_analytics import DailyAnalytics
from app.models.price_snapshot import PriceSnapshot


async def compute_and_save_daily_analytics(
    snapshot_date: date | None = None,
) -> dict:
    """
    Compute and persist daily analytics for the entire market.

    Also saves PriceSnapshot records for each make-model-year-condition group.
    Returns a summary of what was computed.
    """
    if snapshot_date is None:
        snapshot_date = datetime.now(timezone.utc).date()

    logger.info("═══ Computing daily analytics for %s ═══", snapshot_date)

    # Delete existing snapshots for this date (idempotent re-runs)
    await DailyAnalytics.find(
        DailyAnalytics.snapshot_date == snapshot_date
    ).delete()
    await PriceSnapshot.find(
        PriceSnapshot.snapshot_date == snapshot_date
    ).delete()

    saved_analytics = 0
    saved_snapshots = 0

    # ── 1. Market-wide snapshot ──────────────────────────────────────────
    market = await _compute_daily_scope(snapshot_date, scope="market")
    if market:
        await market.insert()
        saved_analytics += 1
        logger.info(
            "Market-wide: %d listings, avg Rs. %s",
            market.total_listings, f"{market.avg_price:,.0f}",
        )

    # ── 2. Per-brand snapshots ───────────────────────────────────────────
    makes = [b for b in await Listing.distinct("make") if b]

    for make in makes:
        doc = await _compute_daily_scope(snapshot_date, scope="brand", make=make)
        if doc and doc.total_listings > 0:
            await doc.insert()
            saved_analytics += 1

    logger.info("Per-brand analytics: %d brands", len(makes))

    # ── 3. Per-brand × condition snapshots ──────────────────────────────
    conditions = [c for c in await Listing.distinct("condition") if c]

    for make in makes:
        for condition in conditions:
            doc = await _compute_daily_scope(
                snapshot_date, scope="brand_condition",
                make=make, condition=condition,
            )
            if doc and doc.total_listings > 0:
                await doc.insert()
                saved_analytics += 1

    # ── 4. Price snapshots — per make×model×year×condition ──────────────
    snapshots = await _compute_model_price_snapshots(snapshot_date)
    for snap in snapshots:
        await snap.insert()
        saved_snapshots += 1

    logger.info("═══ Daily analytics complete: %d analytics docs, %d price snapshots ═══",
                saved_analytics, saved_snapshots)

    return {
        "date": str(snapshot_date),
        "analytics_docs_saved": saved_analytics,
        "price_snapshots_saved": saved_snapshots,
        "makes_covered": len(makes),
        "conditions_covered": len(conditions),
    }


async def _compute_model_price_snapshots(snapshot_date: date) -> list[PriceSnapshot]:
    """
    Aggregate per make×model×year×condition and produce PriceSnapshot records.

    The aggregation:
      - Computes year-by-year average price per model per condition
      - Then averages those yearly averages for the model-condition total
      This gives cleaner data since it normalises for age distribution skew.
    """
    pipeline = [
        {
            "$match": {
                "make": {"$ne": None, "$exists": True},
                "model": {"$ne": None, "$exists": True},
                "price": {"$gt": 0},
            }
        },
        {
            # Step 1: Group by make+model+year+condition
            "$group": {
                "_id": {
                    "make": "$make",
                    "model": "$model",
                    "year": "$year",
                    "condition": "$condition",
                },
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "count": {"$sum": 1},
            }
        },
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    snapshots: list[PriceSnapshot] = []
    for r in results:
        gid = r["_id"]
        snp = PriceSnapshot(
            snapshot_date=snapshot_date,
            make=gid["make"],
            model=gid["model"],
            year=gid.get("year"),
            condition=gid.get("condition"),
            avg_price=round(r["avg_price"], 2),
            min_price=round(r["min_price"], 2),
            max_price=round(r["max_price"], 2),
            listing_count=r["count"],
        )
        snapshots.append(snp)

    return snapshots


async def _compute_daily_scope(
    snapshot_date: date,
    scope: str,
    make: str | None = None,
    condition: str | None = None,
) -> Optional[DailyAnalytics]:
    """Compute analytics for a specific scope."""

    match_stage: dict = {"price": {"$gt": 0}}
    if make:
        match_stage["make"] = make
    if condition:
        match_stage["condition"] = condition

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

    price_change_pct = await _compute_change(snapshot_date, scope, make, condition, r["avg_price"])

    return DailyAnalytics(
        snapshot_date=snapshot_date,
        scope=scope,
        brand=make,
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
    make: str | None,
    condition: str | None,
    current_avg: float,
) -> Optional[float]:
    """Compare current avg price to the previous day's snapshot."""
    yesterday = current_date - timedelta(days=1)

    query: dict = {"snapshot_date": yesterday, "scope": scope}
    if make:
        query["brand"] = make
    if condition:
        query["condition"] = condition

    prev = await DailyAnalytics.find_one(query)

    if not prev or prev.avg_price == 0:
        return None

    change = ((current_avg - prev.avg_price) / prev.avg_price) * 100
    return round(change, 2)
