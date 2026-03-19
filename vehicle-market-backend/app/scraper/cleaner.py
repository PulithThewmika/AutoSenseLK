"""
Data cleaner — normalise currency, mileage units, and other raw fields.
"""

import re
from datetime import date
from typing import Optional

from app.core.logging import logger


def clean_price(raw_price: str) -> Optional[float]:
    """
    Normalise price string to a float value in LKR.

    Handles formats like:
      "Rs 7,800,000"  →  7800000.0
      "7,675,000"     →  7675000.0
      "Rs. 250,000"   →  250000.0
    """
    if not raw_price:
        return None
    cleaned = re.sub(r"[^\d.]", "", raw_price)
    try:
        return float(cleaned)
    except ValueError:
        logger.debug("Could not parse price: %r", raw_price)
        return None


def clean_mileage(raw_mileage: str) -> Optional[float]:
    """
    Normalise mileage to kilometres.

    Handles formats like:
      "165,000 km"  →  165000.0
      "27,160"      →  27160.0
      "50,000 miles" → 80467.0
    """
    if not raw_mileage:
        return None

    is_miles = "mile" in raw_mileage.lower()
    cleaned = re.sub(r"[^\d.]", "", raw_mileage)

    try:
        value = float(cleaned)
        if is_miles:
            value *= 1.60934  # convert miles to km
        return value
    except ValueError:
        logger.debug("Could not parse mileage: %r", raw_mileage)
        return None


def clean_year(raw: str) -> Optional[int]:
    """
    Extract a 4-digit manufacturing year from a string.

    Handles: "2014", "Year of Manufacture: 2014", title strings, etc.
    """
    if not raw:
        return None
    match = re.search(r"\b(19|20)\d{2}\b", raw)
    if match:
        return int(match.group(0))
    return None


def clean_posted_date(raw: str) -> Optional[date]:
    """Parse a posted date ISO string into a date object."""
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except (ValueError, TypeError):
        logger.debug("Could not parse posted_date: %r", raw)
        return None


def clean_listing(raw: dict) -> dict:
    """
    Apply all cleaning steps to a raw listing dict.

    Expects keys produced by the parser (price_raw, mileage_raw, etc.)
    and returns a normalised dict ready for database storage.
    """
    cleaned = dict(raw)  # shallow copy

    # ── Price ────────────────────────────────────────────
    price = clean_price(raw.get("price_raw", ""))
    if price is not None:
        cleaned["price"] = price
    else:
        cleaned["price"] = 0.0
    cleaned.pop("price_raw", None)

    # ── Mileage ─────────────────────────────────────────
    mileage = clean_mileage(raw.get("mileage_raw", ""))
    cleaned["mileage"] = mileage
    cleaned.pop("mileage_raw", None)

    # ── Year ────────────────────────────────────────────
    year_raw = raw.get("year_raw", "") or raw.get("title", "")
    year = clean_year(year_raw)
    cleaned["year"] = year
    cleaned.pop("year_raw", None)

    # ── Posted date ─────────────────────────────────────
    posted = clean_posted_date(raw.get("posted_date_raw", ""))
    cleaned["posted_date"] = posted
    cleaned.pop("posted_date_raw", None)

    # ── Currency ────────────────────────────────────────
    cleaned.setdefault("currency", "LKR")

    # ── Trim whitespace from string fields ──────────────
    for key in ("title", "description", "location", "category",
                "make", "model", "condition"):
        val = cleaned.get(key)
        if isinstance(val, str):
            cleaned[key] = val.strip()

    logger.debug("Cleaned listing: %s", cleaned.get("title", "?"))
    return cleaned
