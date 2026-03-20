"""
Deduplicator — hash-based duplicate detection for listings.
"""

import hashlib

from app.core.logging import logger


async def deduplicate_batch(listings: list[dict]) -> tuple[list[dict], int]:
    """
    Filter a list of listings, returning only new ones or those that have changes.
    Matches primarily on the clean base URL to prevent duplicating ads when price changes.
    """
    new_or_updated: list[dict] = []
    skipped = 0
    from app.models.listing import Listing

    for data in listings:
        # Standardise the URL (remove querystrings like ?page=1 or ?tree.brand)
        raw_url = data.get("source_url", "")
        clean_url = raw_url.split("?")[0] if raw_url else ""
        data["source_url"] = clean_url
        
        # Create a stable identifier hash purely from the URL
        clean_hash = hashlib.sha256(clean_url.encode()).hexdigest()
        data["source_hash"] = clean_hash
        
        # Check if this precise URL is already in our DB
        existing = await Listing.find_one(Listing.source_url == clean_url)
        
        if existing:
            # Ad exists! Inherit its source_hash so storage.py triggers an UPDATE
            data["source_hash"] = existing.source_hash
            
            # Check if any substantive fields have changed
            price_changed = existing.price != data.get("price", 0.0)
            title_changed = existing.title != data.get("title", "")
            
            if price_changed or title_changed:
                new_or_updated.append(data)
                logger.debug("Ad updated (attrs changed): %s", data.get("title", "?"))
            else:
                skipped += 1
        else:
            # Brand new ad
            new_or_updated.append(data)

    logger.info(
        "Deduplication: %d to save/update, %d duplicates skipped",
        len(new_or_updated), skipped,
    )
    return new_or_updated, skipped
