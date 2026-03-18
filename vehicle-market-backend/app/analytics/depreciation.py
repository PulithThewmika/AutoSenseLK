"""
Depreciation curves — price vs age / mileage analysis.
"""

from app.models.listing import Listing


async def depreciation_curve(
    make: str | None = None,
    model: str | None = None,
) -> list[dict]:
    """Return depreciation data points: [{year, avg_price, count}, …]."""
    match_stage: dict = {
        "price": {"$gt": 0},
        "year": {"$ne": None},
    }
    if make:
        match_stage["make_id"] = {"$regex": make, "$options": "i"}
    if model:
        match_stage["model_id"] = {"$regex": model, "$options": "i"}

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": "$year",
                "avg_price": {"$avg": "$price"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    return [
        {
            "year": r["_id"],
            "avg_price": round(r["avg_price"], 2),
            "count": r["count"],
        }
        for r in results
    ]


async def mileage_curve(
    make: str | None = None,
    model: str | None = None,
) -> list[dict]:
    """Return price-vs-mileage data points grouped by mileage bands."""
    match_stage: dict = {
        "price": {"$gt": 0},
        "mileage": {"$ne": None, "$gt": 0},
    }
    if make:
        match_stage["make_id"] = {"$regex": make, "$options": "i"}
    if model:
        match_stage["model_id"] = {"$regex": model, "$options": "i"}

    # Bucket by 25,000 km bands
    pipeline = [
        {"$match": match_stage},
        {
            "$bucket": {
                "groupBy": "$mileage",
                "boundaries": [0, 25000, 50000, 75000, 100000, 150000, 200000, 300000, 500000],
                "default": "500000+",
                "output": {
                    "avg_price": {"$avg": "$price"},
                    "count": {"$sum": 1},
                },
            }
        },
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    return [
        {
            "mileage_band": f"{r['_id']}+" if isinstance(r["_id"], str) else f"{int(r['_id']):,} km",
            "avg_price": round(r["avg_price"], 2),
            "count": r["count"],
        }
        for r in results
    ]
