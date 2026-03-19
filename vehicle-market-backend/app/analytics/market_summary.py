"""
Market summary — overall market statistics and listing counts.
"""

from app.models.listing import Listing


async def market_summary() -> dict:
    """Return aggregate market stats: total listings, avg price, etc."""
    total = await Listing.count()

    if total == 0:
        return {
            "total_listings": 0,
            "avg_price": 0.0,
            "makes_count": 0,
            "models_count": 0,
        }

    # Average price via aggregation
    pipeline = [
        {"$match": {"price": {"$gt": 0}}},
        {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}},
    ]
    cursor = Listing.aggregate(pipeline)
    result = await cursor.to_list()
    avg_price = result[0]["avg_price"] if result else 0.0

    # Distinct makes and models
    makes = [m for m in await Listing.distinct("make") if m]
    models = [m for m in await Listing.distinct("model") if m]

    return {
        "total_listings": total,
        "avg_price": round(avg_price, 2),
        "makes_count": len(makes),
        "models_count": len(models),
    }


async def avg_price_by_make_model(
    make: str | None = None,
    model: str | None = None,
) -> dict:
    """Return average price filtered by optional make/model."""
    match_stage: dict = {"price": {"$gt": 0}}
    if make:
        match_stage["make"] = {"$regex": make, "$options": "i"}
    if model:
        match_stage["model"] = {"$regex": model, "$options": "i"}

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": None,
                "avg_price": {"$avg": "$price"},
                "sample_count": {"$sum": 1},
            }
        },
    ]

    cursor = Listing.aggregate(pipeline)
    result = await cursor.to_list()

    if not result:
        return {
            "make": make,
            "model": model,
            "avg_price": 0.0,
            "sample_count": 0,
        }

    return {
        "make": make,
        "model": model,
        "avg_price": round(result[0]["avg_price"], 2),
        "sample_count": result[0]["sample_count"],
    }
