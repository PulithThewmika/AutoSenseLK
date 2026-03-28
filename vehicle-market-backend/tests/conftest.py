import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.main import create_app
from app.core.config import settings
from app.models.listing import Listing
from app.models.vehicle import Make, Model
from app.models.daily_analytics import DailyAnalytics
from app.models.deal_score import DealScore
from app.models.price_snapshot import PriceSnapshot

@pytest.fixture(autouse=True)
async def setup_test_db():
    # Force use of test DB
    settings.MONGODB_DB_NAME = "vehicle_market_test"
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=db,
        document_models=[
            Make,
            Model,
            Listing,
            DealScore,
            PriceSnapshot,
            DailyAnalytics
        ]
    )
    
    # Drop test collections before tests
    await Make.get_motor_collection().drop()
    await Model.get_motor_collection().drop()
    await Listing.get_motor_collection().drop()
    await DealScore.get_motor_collection().drop()
    await PriceSnapshot.get_motor_collection().drop()
    await DailyAnalytics.get_motor_collection().drop()

    yield
    
    # Clean up after tests are done
    await client.drop_database(settings.MONGODB_DB_NAME)

@pytest.fixture(scope="session")
def app():
    return create_app()

@pytest.fixture
async def async_client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
