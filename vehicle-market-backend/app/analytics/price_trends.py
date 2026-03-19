"""
Price trends — compute monthly average price per model.
Uses PriceSnapshot aggregates (make×model×year×condition) for clean trend data.
"""

from datetime import datetime, timedelta, timezone

from app.models.listing import Listing
from app.models.price_snapshot import PriceSnapshot


async def monthly_avg_price(
    make: str | None = None,
    model: str | None = None,
    months: int = 12,
) -> list[dict]:
    """
    Return a list of {month, avg_price, count} dicts.

    Groups listings by the month they were created and computes
    the average price for each month.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=months * 30)

    match_stage: dict = {
        "price": {"$gt": 0},
        "created_at": {"$gte": cutoff},
    }
    if make:
        match_stage["make"] = {"$regex": make, "$options": "i"}
    if model:
        match_stage["model"] = {"$regex": model, "$options": "i"}

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                },
                "avg_price": {"$avg": "$price"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    trends = []
    for r in results:
        month_str = f"{r['_id']['year']}-{r['_id']['month']:02d}"
        trends.append({
            "month": month_str,
            "avg_price": round(r["avg_price"], 2),
            "count": r["count"],
        })

    return trends


async def model_year_price_history(
    make: str,
    model: str,
    condition: str | None = None,
) -> list[dict]:
    """
    Return average price per manufacture year for a given make/model.

    Uses PriceSnapshot aggregates for cleaner data (removes listing bias).
    Each year entry is averaged across all days to give a stable number.
    """
    match: dict = {
        "make": {"$regex": make, "$options": "i"},
        "model": {"$regex": model, "$options": "i"},
        "year": {"$ne": None},
    }
    if condition:
        match["condition"] = condition

    pipeline = [
        {"$match": match},
        {
            "$group": {
                "_id": "$year",
                "avg_price": {"$avg": "$avg_price"},
                "min_price": {"$min": "$min_price"},
                "max_price": {"$max": "$max_price"},
                "total_listings": {"$sum": "$listing_count"},
                "snapshot_days": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    cursor = PriceSnapshot.aggregate(pipeline)
    results = await cursor.to_list()

    return [
        {
            "year": r["_id"],
            "avg_price": round(r["avg_price"], 2),
            "min_price": round(r["min_price"], 2),
            "max_price": round(r["max_price"], 2),
            "total_listings": r["total_listings"],
        }
        for r in results if r["_id"]
    ]
