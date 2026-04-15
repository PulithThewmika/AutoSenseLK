"""
Celery application instance with Redis broker and Beat schedule.

Beat schedule triggers a single chained pipeline task at midnight:
  daily_pipeline → Scrape (with retry) → Snapshot → Retrain

To start the Beat scheduler alongside the worker:
  celery -A app.tasks.celery_app beat --loglevel=info
  celery -A app.tasks.celery_app worker --loglevel=info
"""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "vehicle_market",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Colombo",
    enable_utc=True,
)

# ── Celery Beat — single chained pipeline at midnight ─
celery_app.conf.beat_schedule = {
    "daily-pipeline-midnight": {
        "task": "daily_pipeline",
        "schedule": crontab(hour=0, minute=0),   # every day at 00:00
        "options": {"queue": "default"},
    },
}
