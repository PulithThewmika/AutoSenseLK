"""
Deal score document model (Beanie / MongoDB) — stores ML-generated score per listing.
"""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class DealScore(Document):
    """ML-predicted deal quality for a listing."""

    listing_id: str  # Reference to Listing document ID
    predicted_price: float
    actual_price: float
    score: float
    label: str  # good_deal / fair / overpriced
    scored_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "deal_scores"
        indexes = ["listing_id"]
