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
    make_id: int | None = None
    model_id: int | None = None


class ListingResponse(ListingBase):
    id: int
    source_url: str
    make_id: int | None = None
    model_id: int | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ListingListResponse(BaseModel):
    page: int
    size: int
    total: int
    results: list[ListingResponse]
