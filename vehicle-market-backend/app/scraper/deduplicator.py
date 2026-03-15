"""
Deduplicator — hash-based duplicate detection for listings.
"""

import hashlib

from app.core.logging import logger


def compute_hash(listing: dict) -> str:
    """Generate a deterministic hash for a listing to detect duplicates."""
    key = (
        f"{listing.get('source_url', '')}|"
        f"{listing.get('title', '')}|"
        f"{listing.get('price', '')}"
    )
    return hashlib.sha256(key.encode()).hexdigest()


async def is_duplicate(listing_hash: str) -> bool:
    """Check whether a listing with this hash already exists in the DB."""
    from app.models.listing import Listing

    existing = await Listing.find_one(Listing.source_hash == listing_hash)
    return existing is not None


async def deduplicate_batch(listings: list[dict]) -> tuple[list[dict], int]:
    """
    Filter a list of listings, returning only new or updated ones.

    Returns:
        (new_listings, skipped_count)
    """
    new_listings: list[dict] = []
    skipped = 0

    for listing in listings:
        h = compute_hash(listing)
        listing["source_hash"] = h

        if await is_duplicate(h):
            skipped += 1
            logger.debug("Duplicate skipped: %s", listing.get("title", "?"))
        else:
            new_listings.append(listing)

    logger.info(
        "Deduplication: %d new, %d duplicates skipped",
        len(new_listings), skipped,
    )
    return new_listings, skipped
