"""
ML Scorer — label listings as good deal / fair / overpriced.
"""


def score_listing(predicted_price: float, actual_price: float) -> dict:
    """Compare predicted vs actual price and return a label + score."""
    if actual_price == 0:
        return {"score": 0.0, "label": "unknown"}

    ratio = actual_price / predicted_price

    if ratio < 0.85:
        label = "good_deal"
    elif ratio <= 1.15:
        label = "fair"
    else:
        label = "overpriced"

    return {"score": round(ratio, 4), "label": label}
