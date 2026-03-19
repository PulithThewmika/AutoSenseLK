"""
Makes & models endpoints.
- GET /makes              — list all vehicle makes (from DB)
- GET /makes/{name}/models  — models for a given make (with listing counts)
- GET /makes/{make}/models/{model}/years — year-by-year price history
"""

from fastapi import APIRouter

from app.models.vehicle import Make, Model
from app.models.listing import Listing
from app.analytics.price_trends import model_year_price_history

router = APIRouter(prefix="/makes", tags=["makes"])


@router.get("/")
async def list_makes():
    """Return all vehicle makes from the database (seeded from brand registry)."""
    makes = await Make.find_all().sort("+name").to_list()

    if makes:
        return {
            "makes": [{"name": m.name, "slug": m.slug, "scrape_url": m.scrape_url} for m in makes],
            "total": len(makes),
        }

    # Fallback: derive from listings if seed hasn't run yet
    raw_makes = sorted([m for m in await Listing.distinct("make") if m])
    return {
        "makes": [{"name": m} for m in raw_makes],
        "total": len(raw_makes),
    }


@router.get("/{make_name}/models")
async def list_models(make_name: str):
    """Return all models for a make with listing counts."""
    # Try DB-seeded models first
    db_models = await Model.find(
        Model.make_slug == make_name.lower()
    ).sort("+name").to_list()

    if db_models:
        # Enrich with live listing counts
        pipeline = [
            {"$match": {"make": {"$regex": make_name, "$options": "i"}, "model": {"$ne": None}}},
            {"$group": {"_id": "$model", "count": {"$sum": 1}}},
        ]
        cursor = Listing.aggregate(pipeline)
        count_results = await cursor.to_list()
        counts = {r["_id"]: r["count"] for r in count_results}

        return {
            "make": make_name,
            "models": [
                {
                    "name": m.name,
                    "slug": m.slug,
                    "scrape_url": m.scrape_url,
                    "listing_count": counts.get(m.name, 0),
                }
                for m in db_models
            ],
            "total": len(db_models),
        }

    # Fallback: derive from listings
    pipeline = [
        {"$match": {"make": {"$regex": make_name, "$options": "i"}, "model": {"$ne": None}}},
        {"$group": {"_id": "$model", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()
    models = [{"name": r["_id"], "listing_count": r["count"]} for r in results if r["_id"]]

    return {"make": make_name, "models": models, "total": len(models)}


@router.get("/{make_name}/models/{model_name}/years")
async def model_year_history(
    make_name: str,
    model_name: str,
    condition: str | None = None,
):
    """Return year-by-year average price history for a make/model."""
    data = await model_year_price_history(make_name, model_name, condition)
    return {
        "make": make_name,
        "model": model_name,
        "condition": condition,
        "data": data,
    }
