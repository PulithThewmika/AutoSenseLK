"""
Pydantic response schema for deal scoring.
"""

from pydantic import BaseModel


class DealScoreResponse(BaseModel):
    listing_id: int
    predicted_price: float
    actual_price: float
    score: float
    label: str  # good_deal | fair | overpriced
