"""
Data cleaner — normalise currency, mileage units, and other raw fields.
"""


def clean_price(raw_price: str) -> float:
    """Normalise price string to a float value in LKR."""
    # TODO: strip currency symbols, commas, convert if needed
    return 0.0


def clean_mileage(raw_mileage: str) -> float:
    """Normalise mileage to kilometres."""
    # TODO: handle 'km', 'miles' etc.
    return 0.0


def clean_listing(raw: dict) -> dict:
    """Apply all cleaning steps to a raw listing dict."""
    # TODO: orchestrate individual cleaners
    return raw
