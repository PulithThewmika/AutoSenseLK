"""
MongoDB connection via Motor (async driver) + Beanie ODM.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings


async def init_db() -> None:
    """Initialize the MongoDB connection and Beanie ODM."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

    # Import all document models here
    from app.models.listing import Listing
    from app.models.vehicle import Make, Model
    from app.models.price_snapshot import PriceSnapshot
    from app.models.deal_score import DealScore
    from app.models.daily_analytics import DailyAnalytics

    await init_beanie(
        database=db,
        document_models=[Listing, Make, Model, PriceSnapshot, DealScore, DailyAnalytics],
    )
