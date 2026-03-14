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

    # ── Database ─────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/vehicle_market"

    # ── Redis / Celery ───────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Security ─────────────────────────────────────────
    API_KEY: str = ""
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
