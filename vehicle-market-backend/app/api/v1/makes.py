"""
Makes & models endpoints.
- GET /makes              — list all vehicle makes
- GET /makes/{id}/models  — models for a given make
"""

from fastapi import APIRouter

from app.models.listing import Listing

router = APIRouter(prefix="/makes", tags=["makes"])


@router.get("/")
async def list_makes():
    """Return all known vehicle makes (extracted from listings)."""
    makes = await Listing.distinct("make_id")
    # Filter out None/empty values and sort
    makes = sorted([m for m in makes if m])
    return {
        "makes": [{"name": m} for m in makes],
        "total": len(makes),
    }


@router.get("/{make_name}/models")
async def list_models(make_name: str):
    """Return all models belonging to a make (extracted from listings)."""
    # Find distinct model_ids where make_id matches
    pipeline = [
        {"$match": {"make_id": {"$regex": make_name, "$options": "i"}, "model_id": {"$ne": None}}},
        {"$group": {"_id": "$model_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    cursor = Listing.aggregate(pipeline)
    results = await cursor.to_list()

    models = [{"name": r["_id"], "listing_count": r["count"]} for r in results if r["_id"]]

    return {
        "make": make_name,
        "models": models,
        "total": len(models),
    }
