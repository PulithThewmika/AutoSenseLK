"""
Deal-score endpoints.
- GET /deals/score?listing_id=  — deal quality for a listing
"""

from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId

from app.models.listing import Listing
from app.models.deal_score import DealScore
from app.ml.scorer import score_listing

router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("/score")
async def deal_score(listing_id: str = Query(...)):
    """Return the deal score (good / fair / overpriced) for a listing."""
    # 1. Fetch the listing
    try:
        listing = await Listing.get(PydanticObjectId(listing_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Listing not found")

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    # 2. Check for existing score
    existing = await DealScore.find_one(DealScore.listing_id == listing_id)
    if existing:
        return {
            "listing_id": listing_id,
            "predicted_price": existing.predicted_price,
            "actual_price": existing.actual_price,
            "score": existing.score,
            "label": existing.label,
        }

    # 3. Compute predicted price as avg of similar listings (same make/model)
    predicted_price = await _compute_avg_price(listing.make, listing.model)

    if predicted_price == 0.0:
        return {
            "listing_id": listing_id,
            "predicted_price": 0.0,
            "actual_price": listing.price,
            "score": 0.0,
            "label": "unknown",
        }

    # 4. Score the deal
    result = score_listing(predicted_price, listing.price)

    # 5. Persist the score
    deal = DealScore(
        listing_id=listing_id,
        predicted_price=predicted_price,
        actual_price=listing.price,
        score=result["score"],
        label=result["label"],
    )
    await deal.insert()

    return {
        "listing_id": listing_id,
        "predicted_price": round(predicted_price, 2),
        "actual_price": listing.price,
        "score": result["score"],
        "label": result["label"],
    }


async def _compute_avg_price(
    make: str | None,
    model: str | None,
) -> float:
    """Compute the average price from similar listings as a price proxy."""
    match_stage: dict = {"price": {"$gt": 0}}

    if make:
        match_stage["make"] = make
    if model:
        match_stage["model"] = model

    # If we don't have both make and model, fall back to just make
    if not make and not model:
        return 0.0

    pipeline = [
        {"$match": match_stage},
        {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}},
    ]

    cursor = Listing.aggregate(pipeline)
    result = await cursor.to_list()

    return result[0]["avg_price"] if result else 0.0
