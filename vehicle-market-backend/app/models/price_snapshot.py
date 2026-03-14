"""
Historical price snapshot document model (Beanie / MongoDB).
"""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class PriceSnapshot(Document):
    """Daily snapshot of a listing's price for trend analysis."""

    listing_id: str  # Reference to Listing document ID
    price: float
    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "price_snapshots"
        indexes = ["listing_id", "captured_at"]
