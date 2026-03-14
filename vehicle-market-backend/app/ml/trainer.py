"""
ML Trainer — train a regression model on historical listings.
"""

from app.core.logging import logger


def train_model() -> None:
    """Train (or retrain) the price-prediction model on current listings."""
    logger.info("Starting model training …")
    # TODO: load data → feature engineering → train → evaluate → save
    logger.info("Model training complete.")
