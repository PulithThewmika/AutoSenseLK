"""
Pydantic response schemas for analytics endpoints.
"""

from pydantic import BaseModel


class AvgPriceResponse(BaseModel):
    make: str | None = None
    model: str | None = None
    avg_price: float
    sample_count: int


class PriceTrendPoint(BaseModel):
    month: str  # e.g. "2026-01"
    avg_price: float
    count: int


class PriceTrendResponse(BaseModel):
    make: str | None = None
    model: str | None = None
    trends: list[PriceTrendPoint]
