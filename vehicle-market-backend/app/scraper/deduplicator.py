"""
Deduplicator — hash-based duplicate detection for listings.
"""

import hashlib


def compute_hash(listing: dict) -> str:
    """Generate a deterministic hash for a listing to detect duplicates."""
    key = f"{listing.get('source_url', '')}|{listing.get('title', '')}|{listing.get('price', '')}"
    return hashlib.sha256(key.encode()).hexdigest()


def is_duplicate(listing_hash: str) -> bool:
    """Check whether a listing with this hash already exists in the DB."""
    # TODO: query DB for existing hash
    return False
