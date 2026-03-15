"""
Listing document model (Beanie / MongoDB).
"""

from datetime import datetime, timezone
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
    make_id: Optional[str] = None
    model_id: Optional[str] = None

    # Additional fields from detail pages
    category: Optional[str] = None        # Cars, Motorbikes, Vans, etc.
    transmission: Optional[str] = None     # Manual, Automatic
    fuel_type: Optional[str] = None        # Petrol, Diesel, Hybrid, Electric
    engine_capacity: Optional[str] = None  # e.g. "1500 cc"
    condition: Optional[str] = None        # New, Used
    seller_name: Optional[str] = None
    image_urls: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "listings"
        indexes = ["source_url", "source_hash", "make_id", "model_id"]
