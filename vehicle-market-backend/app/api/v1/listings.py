"""
Listings endpoints.
- GET /listings          — paginated list with filters
- GET /listings/{id}     — single listing detail
"""

from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("/")
async def get_listings(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    make: str | None = None,
    model: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
):
    """Return paginated vehicle listings with optional filters."""
    # TODO: query DB with filters & pagination
    return {"page": page, "size": size, "results": []}


@router.get("/{listing_id}")
async def get_listing(listing_id: int):
    """Return a single listing by ID."""
    # TODO: fetch from DB
    return {"listing_id": listing_id}
