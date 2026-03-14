"""
Celery task — retrain ML model periodically.
"""

from app.tasks.celery_app import celery_app
from app.ml.trainer import train_model


@celery_app.task(name="retrain_model")
def retrain_model_task() -> str:
    """Retrain the price-prediction model as a background Celery task."""
    train_model()
    return "Model retraining completed"
