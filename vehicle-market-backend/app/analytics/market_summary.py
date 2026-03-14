"""
Market summary — overall market statistics and listing counts.
"""


async def market_summary() -> dict:
    """Return aggregate market stats: total listings, avg price, etc."""
    # TODO: aggregate from listings table
    return {
        "total_listings": 0,
        "avg_price": 0.0,
        "makes_count": 0,
        "models_count": 0,
    }
