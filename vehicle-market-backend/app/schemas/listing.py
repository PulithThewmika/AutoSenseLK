"""
Pydantic request/response schemas for listings.
"""

from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ListingBase(BaseModel):
    title: str
    price: float
    currency: str = "LKR"
    mileage: float | None = None
    year: int | None = None
    location: str | None = None


class ListingCreate(ListingBase):
    source_url: HttpUrl
    make: str | None = None
    model: str | None = None
    condition: str | None = None


class ListingResponse(ListingBase):
    id: str
    source_url: str
    make: str | None = None
    model: str | None = None
    condition: str | None = None
    category: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ListingListResponse(BaseModel):
    page: int
    size: int
    total: int
    results: list[ListingResponse]
