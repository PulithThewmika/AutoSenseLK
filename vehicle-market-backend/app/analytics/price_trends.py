"""
Price trends — compute monthly average price per model.
"""

from datetime import datetime, timedelta, timezone

from app.models.listing import Listing


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
        match_stage["make_id"] = {"$regex": make, "$options": "i"}
    if model:
        match_stage["model_id"] = {"$regex": model, "$options": "i"}

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
