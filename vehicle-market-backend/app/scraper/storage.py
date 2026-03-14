"""
Storage — persist cleaned listings into the database.
"""

from app.core.logging import logger


async def save_listings(listings: list[dict]) -> int:
    """Insert or update cleaned listings in the DB. Returns count saved."""
    # TODO: bulk upsert via SQLAlchemy
    logger.info("Saving %d listings …", len(listings))
    return 0
