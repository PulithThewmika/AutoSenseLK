"""
Deal-score endpoints.
- GET /deals/score?listing_id=  — deal quality for a listing
"""

from fastapi import APIRouter, Query

router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("/score")
async def deal_score(listing_id: int = Query(...)):
    """Return the deal score (good / fair / overpriced) for a listing."""
    # TODO: look up ML-generated score
    return {"listing_id": listing_id, "score": None, "label": "unknown"}
