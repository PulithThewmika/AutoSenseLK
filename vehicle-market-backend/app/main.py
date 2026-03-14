"""
FastAPI application factory and router mounting.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import listings, analytics, deals, makes, search


def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Vehicle Market Intelligence API — scrape, analyse, and score Sri Lankan vehicle listings.",
    )

    # ── CORS ─────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── API v1 routers ───────────────────────────────────
    api_prefix = "/api/v1"
    app.include_router(listings.router, prefix=api_prefix)
    app.include_router(analytics.router, prefix=api_prefix)
    app.include_router(deals.router, prefix=api_prefix)
    app.include_router(makes.router, prefix=api_prefix)
    app.include_router(search.router, prefix=api_prefix)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
