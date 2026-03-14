"""
Full-text search endpoint.
- GET /search?q=  — search listings by keyword
"""

from fastapi import APIRouter, Query

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
async def search_listings(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """Full-text search across listings."""
    # TODO: implement full-text search (PostgreSQL tsvector or ElasticSearch)
    return {"query": q, "page": page, "size": size, "results": []}
