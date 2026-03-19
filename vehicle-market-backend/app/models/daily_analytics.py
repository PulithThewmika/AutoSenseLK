"""
Daily analytics snapshot document model (Beanie / MongoDB).

Persists daily market statistics at three levels:
  - market   → overall market snapshot
  - brand    → per-brand totals
  - brand_condition → per-brand × per-condition
"""

from datetime import date, datetime, timezone
from typing import Optional

from beanie import Document
from pydantic import Field


class DailyAnalytics(Document):
    """Daily market analytics snapshot."""

    snapshot_date: date
    scope: str                            # "market", "brand", "brand_condition"
    brand: Optional[str] = None           # make name (None for market-wide)
    condition: Optional[str] = None       # used / brand_new / reconditioned

    total_listings: int = 0
    avg_price: float = 0.0
    min_price: float = 0.0
    max_price: float = 0.0
    median_price: float = 0.0
    price_change_pct: Optional[float] = None  # vs previous day

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "daily_analytics"
        indexes = [
            [("snapshot_date", -1), ("scope", 1), ("brand", 1), ("condition", 1)],
        ]
