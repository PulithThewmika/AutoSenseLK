"""
Celery application instance with Redis broker and Beat schedule.

Beat schedule triggers:
  - scrape_listings   → every day at 00:00 (midnight) Asia/Colombo
  - snapshot_prices   → every day at 05:00 Asia/Colombo
  - retrain_model     → every day at 06:00 Asia/Colombo

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

# ── Celery Beat — periodic task schedule ─────────────
celery_app.conf.beat_schedule = {
    "daily-scrape-midnight": {
        "task": "scrape_listings",
        "schedule": crontab(hour=0, minute=0),   # every day at 00:00
        "options": {"queue": "default"},
    },
    "daily-snapshot-5am": {
        "task": "snapshot_prices",
        "schedule": crontab(hour=5, minute=0),    # every day at 05:00
    },
    "daily-retrain-6am": {
        "task": "retrain_model",
        "schedule": crontab(hour=6, minute=0),    # every day at 06:00
    },
}
