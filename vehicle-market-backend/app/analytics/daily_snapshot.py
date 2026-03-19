"""
Daily analytics snapshot engine.

Produces daily DailyAnalytics documents and PriceSnapshot aggregates
at four levels:
  1. Market-wide   → 1 document per day
  2. Per-brand     → 1 per make per day
  3. Per-brand × condition → 1 per make × condition per day
  4. Per-brand × model × year × condition → most granular, for trend analysis

Includes:
  - IQR-based outlier filtering (removes extreme prices that skew analytics)
  - posted_date-based day-by-day analysis (analyses only same-day listings)
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Optional

from app.core.logging import logger
from app.models.listing import Listing
from app.models.daily_analytics import DailyAnalytics
from app.models.price_snapshot import PriceSnapshot


# ── Configuration ──────────────────────────────────────────────────────────
MIN_LISTINGS_FOR_ANALYTICS = 2     # Groups with fewer listings are skipped
IQR_MULTIPLIER = 1.5              # Tukey fence for outlier detection


async def compute_and_save_daily_analytics(
    snapshot_date: date | None = None,
) -> dict:
    """
    Compute and persist daily analytics for the entire market.

    Uses posted_date to only include listings posted on the snapshot date.
    Applies IQR-based outlier filtering for clean analytics.
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

    Steps:
      1. Match listings with valid prices (posted on snapshot_date if available)
      2. Group by make+model+year+condition
      3. For each group, apply IQR filtering to remove outliers
      4. Skip groups with too few listings
    """
    # Build match filter — prefer posted_date, fall back to all listings
    match_filter: dict = {
        "make": {"$ne": None, "$exists": True},
        "model": {"$ne": None, "$exists": True},
        "price": {"$gt": 0},
    }

    # Check if we have listings with posted_date for this date
    dated_count = await Listing.find(
        Listing.posted_date == snapshot_date,
        Listing.price > 0,
    ).count()

    if dated_count >= MIN_LISTINGS_FOR_ANALYTICS:
        match_filter["posted_date"] = snapshot_date
        logger.info("Using %d listings posted on %s for snapshots", dated_count, snapshot_date)
    else:
        logger.info("Only %d dated listings for %s — using all listings for snapshots", dated_count, snapshot_date)

    pipeline = [
        {"$match": match_filter},
        {
            "$group": {
                "_id": {
                    "make": "$make",
                    "model": "$model",
                    "year": "$year",
                    "condition": "$condition",
                },
                "prices": {"$push": "$price"},
                "count": {"$sum": 1},
            }
        },
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    snapshots: list[PriceSnapshot] = []
    skipped_outlier = 0

    for r in results:
        gid = r["_id"]
        prices = sorted(r["prices"])

        # Skip groups with too few listings
        if len(prices) < MIN_LISTINGS_FOR_ANALYTICS:
            continue

        # Apply IQR outlier filtering
        cleaned_prices = _remove_outliers_iqr(prices)
        if len(cleaned_prices) < 1:
            skipped_outlier += 1
            continue

        snp = PriceSnapshot(
            snapshot_date=snapshot_date,
            make=gid["make"],
            model=gid["model"],
            year=gid.get("year"),
            condition=gid.get("condition"),
            avg_price=round(sum(cleaned_prices) / len(cleaned_prices), 2),
            min_price=round(min(cleaned_prices), 2),
            max_price=round(max(cleaned_prices), 2),
            listing_count=len(cleaned_prices),
        )
        snapshots.append(snp)

    if skipped_outlier:
        logger.info("Skipped %d groups (all outliers after IQR filter)", skipped_outlier)

    return snapshots


def _remove_outliers_iqr(prices: list[float]) -> list[float]:
    """
    Remove outliers using the Interquartile Range (IQR) method.

    Keeps only prices within [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    This filters out abnormally low (e.g. price=1, test listings) and
    abnormally high prices that would skew the average.
    """
    n = len(prices)
    if n < 4:
        return prices  # Not enough data for IQR

    sorted_p = sorted(prices)
    q1 = sorted_p[n // 4]
    q3 = sorted_p[(3 * n) // 4]
    iqr = q3 - q1

    if iqr == 0:
        return sorted_p  # All values are similar — keep them

    lower = q1 - IQR_MULTIPLIER * iqr
    upper = q3 + IQR_MULTIPLIER * iqr

    return [p for p in sorted_p if lower <= p <= upper]


async def _compute_daily_scope(
    snapshot_date: date,
    scope: str,
    make: str | None = None,
    condition: str | None = None,
) -> Optional[DailyAnalytics]:
    """Compute analytics for a specific scope with outlier filtering."""

    match_stage: dict = {"price": {"$gt": 0}}
    if make:
        match_stage["make"] = make
    if condition:
        match_stage["condition"] = condition

    # Prefer posted_date filtering for day-by-day analysis
    dated_count = 0
    dated_query: dict = {**match_stage, "posted_date": snapshot_date}
    dated_count = await Listing.find(dated_query).count()

    if dated_count >= MIN_LISTINGS_FOR_ANALYTICS:
        match_stage["posted_date"] = snapshot_date

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": None,
                "total": {"$sum": 1},
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

    if len(prices) < MIN_LISTINGS_FOR_ANALYTICS:
        return None

    # Apply IQR outlier filtering
    cleaned = _remove_outliers_iqr(prices)
    if not cleaned:
        return None

    n = len(cleaned)
    avg_price = sum(cleaned) / n
    median = cleaned[n // 2] if n % 2 == 1 else (cleaned[n // 2 - 1] + cleaned[n // 2]) / 2

    price_change_pct = await _compute_change(snapshot_date, scope, make, condition, avg_price)

    return DailyAnalytics(
        snapshot_date=snapshot_date,
        scope=scope,
        brand=make,
        condition=condition,
        total_listings=n,
        avg_price=round(avg_price, 2),
        min_price=round(min(cleaned), 2),
        max_price=round(max(cleaned), 2),
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
