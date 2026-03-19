"""
Listings endpoints.
- GET /listings          — paginated list with filters
- GET /listings/{id}     — single listing detail
"""

from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId

from app.models.listing import Listing

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
    # Build query filter
    query: dict = {}

    if make:
        query["make"] = {"$regex": make, "$options": "i"}
    if model:
        query["model"] = {"$regex": model, "$options": "i"}
    if min_price is not None or max_price is not None:
        price_filter: dict = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price"] = price_filter
    if year_from is not None or year_to is not None:
        year_filter: dict = {}
        if year_from is not None:
            year_filter["$gte"] = year_from
        if year_to is not None:
            year_filter["$lte"] = year_to
        query["year"] = year_filter

    # Count total matching
    total = await Listing.find(query).count()

    # Paginate
    skip = (page - 1) * size
    listings = (
        await Listing.find(query)
        .sort(-Listing.created_at)
        .skip(skip)
        .limit(size)
        .to_list()
    )

    return {
        "page": page,
        "size": size,
        "total": total,
        "results": [_serialize_listing(l) for l in listings],
    }


@router.get("/{listing_id}")
async def get_listing(listing_id: str):
    """Return a single listing by ID."""
    try:
        listing = await Listing.get(PydanticObjectId(listing_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Listing not found")

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    return _serialize_listing(listing)


def _serialize_listing(listing: Listing) -> dict:
    """Convert a Listing document to a JSON-safe dict."""
    return {
        "id": str(listing.id),
        "title": listing.title,
        "description": listing.description,
        "price": listing.price,
        "currency": listing.currency,
        "mileage": listing.mileage,
        "year": listing.year,
        "location": listing.location,
        "source_url": listing.source_url,
        "make": listing.make,
        "model": listing.model,
        "condition": listing.condition,
        "category": listing.category,
        "created_at": listing.created_at.isoformat() if listing.created_at else None,
        "updated_at": listing.updated_at.isoformat() if listing.updated_at else None,
    }
