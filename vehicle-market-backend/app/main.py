"""
FastAPI application factory and router mounting.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import init_db
from app.scraper.seeder import seed_makes_and_models
from app.api.v1 import listings, analytics, deals, makes, search
from app.api.v1 import scrape


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle — initialise MongoDB on boot."""
    await init_db()
    await seed_makes_and_models()   # upsert brand/model registry into DB
    yield


def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Vehicle Market Intelligence API — scrape, analyse, and score Sri Lankan vehicle listings.",
        lifespan=lifespan,
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
    app.include_router(scrape.router, prefix=api_prefix)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
