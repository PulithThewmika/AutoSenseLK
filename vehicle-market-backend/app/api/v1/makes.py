"""
Makes & models endpoints.
- GET /makes              — list all vehicle makes
- GET /makes/{id}/models  — models for a given make
"""

from fastapi import APIRouter

router = APIRouter(prefix="/makes", tags=["makes"])


@router.get("/")
async def list_makes():
    """Return all known vehicle makes."""
    # TODO: query from DB
    return {"makes": []}


@router.get("/{make_id}/models")
async def list_models(make_id: int):
    """Return all models belonging to a make."""
    # TODO: query from DB
    return {"make_id": make_id, "models": []}
