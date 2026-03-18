"""
Full-text search endpoint.
- GET /search?q=  — search listings by keyword
"""

from fastapi import APIRouter, Query

from app.models.listing import Listing

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
async def search_listings(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """Search listings by keyword across title and description."""
    # Use $regex for case-insensitive text search
    query = {
        "$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"make_id": {"$regex": q, "$options": "i"}},
            {"model_id": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}},
            {"location": {"$regex": q, "$options": "i"}},
        ]
    }

    total = await Listing.find(query).count()

    skip = (page - 1) * size
    listings = (
        await Listing.find(query)
        .sort(-Listing.created_at)
        .skip(skip)
        .limit(size)
        .to_list()
    )

    return {
        "query": q,
        "page": page,
        "size": size,
        "total": total,
        "results": [
            {
                "id": str(l.id),
                "title": l.title,
                "price": l.price,
                "currency": l.currency,
                "mileage": l.mileage,
                "year": l.year,
                "location": l.location,
                "make_id": l.make_id,
                "model_id": l.model_id,
                "category": l.category,
                "source_url": l.source_url,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
            for l in listings
        ],
    }
