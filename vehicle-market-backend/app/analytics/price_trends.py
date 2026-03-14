"""
Price trends — compute monthly average price per model.
"""


async def monthly_avg_price(make: str | None = None, model: str | None = None, months: int = 12) -> list[dict]:
    """Return a list of {month, avg_price, count} dicts."""
    # TODO: query price_snapshots grouped by month
    return []
