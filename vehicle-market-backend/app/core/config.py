"""
Application settings loaded from environment variables via Pydantic.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration — reads from .env automatically."""

    # ── App ──────────────────────────────────────────────
    APP_NAME: str = "Vehicle Market API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # ── MongoDB ──────────────────────────────────────────
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "vehicle_market"

    # ── Redis / Celery ───────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Security ─────────────────────────────────────────
    API_KEY: str = ""
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Scraper ──────────────────────────────────────────
    SCRAPE_BASE_URL: str = "https://ikman.lk"
    SCRAPE_MAX_PAGES: int = 5                # legacy — full generic crawl
    SCRAPE_MAX_PAGES_PER_BRAND: int = 3      # pages per brand×condition combo
    SCRAPE_DELAY: float = 1.5
    SCRAPE_USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
    SCRAPE_DETAIL_PAGES: bool = True  # fetch individual ad pages for richer data

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
