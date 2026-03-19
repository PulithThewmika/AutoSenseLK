"""
Listing document model (Beanie / MongoDB).
"""

from datetime import datetime, timezone, date
from typing import Optional

from beanie import Document
from pydantic import Field


class Listing(Document):
    """A single vehicle listing scraped from the marketplace."""

    title: str
    description: Optional[str] = None
    price: float
    currency: str = "LKR"
    mileage: Optional[float] = None
    year: Optional[int] = None
    location: Optional[str] = None
    source_url: str
    source_hash: str

    # Brand / model (plain strings — populated from scrape context)
    make: Optional[str] = None    # e.g. "Toyota"
    model: Optional[str] = None   # e.g. "Aqua"

    # Scrape context
    condition: Optional[str] = None   # used | brand_new | reconditioned
    category: Optional[str] = None   # Cars, Vans, etc.

    # When the ad was posted on ikman.lk
    posted_date: Optional[date] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "listings"
        indexes = [
            "source_url",
            "source_hash",
            "make",
            "model",
            "condition",
            "year",
            "posted_date",
            [("make", 1), ("model", 1), ("year", 1), ("condition", 1)],  # primary analytics index
            [("make", 1), ("condition", 1)],
            [("posted_date", -1), ("make", 1)],  # day-by-day analysis
        ]
