"""
Storage — persist cleaned listings into the database.
"""

from datetime import datetime, timezone

from app.core.logging import logger
from app.models.listing import Listing


async def save_listings(listings: list[dict]) -> int:
    """
    Insert or update cleaned listings in the DB.

    Uses ``source_hash`` as the unique key for upsert logic.
    Returns count of successfully saved listings.
    """
    saved = 0

    for data in listings:
        try:
            source_hash = data.get("source_hash", "")

            # Check if this listing already exists (update scenario)
            existing = await Listing.find_one(
                Listing.source_hash == source_hash
            ) if source_hash else None

            if existing:
                # Update existing listing
                for key, value in data.items():
                    if key not in ("source_hash", "created_at") and value is not None:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now(timezone.utc)
                await existing.save()
                saved += 1
                logger.debug("Updated listing: %s", existing.title)
            else:
                # Insert new listing
                listing = Listing(
                    title=data.get("title", ""),
                    description=data.get("description"),
                    price=data.get("price", 0.0),
                    currency=data.get("currency", "LKR"),
                    mileage=data.get("mileage"),
                    year=data.get("year"),
                    location=data.get("location"),
                    source_url=data.get("source_url", ""),
                    source_hash=data.get("source_hash", ""),
                    make=data.get("make"),
                    model=data.get("model"),
                    condition=data.get("condition"),
                    category=data.get("category"),
                )
                await listing.insert()
                saved += 1
                logger.debug("Inserted listing: %s", listing.title)

        except Exception as exc:
            logger.error("Failed to save listing %s: %s",
                         data.get("title", "?"), exc)

    logger.info("Saved %d / %d listings to database", saved, len(listings))
    return saved
