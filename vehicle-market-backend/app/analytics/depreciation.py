"""
Depreciation curves — price vs age / mileage analysis.
"""


async def depreciation_curve(make: str | None = None, model: str | None = None) -> list[dict]:
    """Return depreciation data points: [{year, avg_price}, …]."""
    # TODO: compute from listings grouped by year
    return []


async def mileage_curve(make: str | None = None, model: str | None = None) -> list[dict]:
    """Return price-vs-mileage data points."""
    # TODO: compute from listings grouped by mileage bands
    return []
