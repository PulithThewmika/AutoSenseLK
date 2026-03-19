"""
Historical price snapshot document model (Beanie / MongoDB).
"""

from datetime import date, datetime, timezone
from typing import Optional

from beanie import Document
from pydantic import Field


class PriceSnapshot(Document):
    """
    Daily price snapshot for a specific make-model-year-condition combination.

    One document per unique (make, model, year, condition) group per day,
    storing the average price across all active listings in that group.
    """

    snapshot_date: date
    make: str
    model: str
    year: Optional[int] = None
    condition: Optional[str] = None       # used | brand_new | reconditioned

    avg_price: float
    min_price: float
    max_price: float
    listing_count: int

    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "price_snapshots"
        indexes = [
            [("snapshot_date", -1), ("make", 1), ("model", 1), ("year", 1), ("condition", 1)],
            [("make", 1), ("model", 1)],
        ]
