# Scheduler & Daily Pipeline

> **Trigger**: Every day at **00:00 (midnight)** Asia/Colombo  
> **Engine**: APScheduler (in-process) + Celery Beat (optional)  
> **Config**: `app/tasks/scheduler.py` (primary) | `app/tasks/celery_app.py` (Celery alternative)

---

## Pipeline Overview

The system runs a **chained daily pipeline** where each step depends on the previous one completing successfully:

```
00:00 (midnight)
    │
    ▼
┌──────────────────────────────────────────┐
│  Step 1: SCRAPE CYCLE                     │
│  Crawl all 56 brands × 546 models × 3    │
│  conditions from ikman.lk                 │
│                                           │
│  ⟳ Retry: up to 3 attempts               │
│  ⏱ Delay: 5 min between retries          │
│  ✗ If all retries fail → pipeline ABORTS  │
└────────────────┬─────────────────────────┘
                 │ on success
                 ▼
┌──────────────────────────────────────────┐
│  Step 2: DAILY SNAPSHOT                   │
│  Compute analytics at 4 levels:           │
│  • Market-wide summary                    │
│  • Per-brand breakdown                    │
│  • Per-brand × condition                  │
│  • Per-make × model × year × condition    │
│                                           │
│  ✗ If fails → retrain is SKIPPED          │
└────────────────┬─────────────────────────┘
                 │ on success
                 ▼
┌──────────────────────────────────────────┐
│  Step 3: MODEL RETRAIN                    │
│  Retrain ML price-prediction model        │
│  using latest scraped data                │
└──────────────────────────────────────────┘
```

---

## Retry Logic (Scrape Step)

The scrape cycle is the most failure-prone step (network errors, rate limiting, site downtime), so it has built-in retry logic:

| Setting | Value | Description |
|---|---|---|
| `MAX_SCRAPE_RETRIES` | `3` | Maximum number of attempts |
| `RETRY_DELAY_SECONDS` | `300` (5 min) | Wait time between retries |
| `misfire_grace_time` | `3600` (1 hour) | If server was down at midnight, still runs if started within 1 hour |

### Retry Flow

```
Attempt 1 (00:00)
    ├─ Success → continue to Snapshot
    └─ Failure → wait 5 min
        │
Attempt 2 (00:05)
    ├─ Success → continue to Snapshot
    └─ Failure → wait 5 min
        │
Attempt 3 (00:10)
    ├─ Success → continue to Snapshot
    └─ Failure → PIPELINE ABORTED (logged as error)
```

### Failure Scenarios

| Scenario | Behaviour |
|---|---|
| Scrape fails, retry succeeds | Pipeline continues normally |
| All 3 scrape retries fail | Pipeline **aborts**, snapshot & retrain are **skipped** |
| Scrape succeeds, snapshot fails | Retrain is **skipped**, partial result logged |
| Scrape + snapshot succeed, retrain fails | Scraped data & analytics are **preserved**, only ML model is stale |
| Server down at midnight | Runs when server starts (within 1-hour grace window) |

---

## Architecture: Two Scheduler Engines

The system supports **two scheduling engines**. Only one needs to be active:

### 1. APScheduler (Default — In-Process)

Runs inside the FastAPI process. **No extra services needed.**

```
┌─────────────────────────────────────┐
│  FastAPI Process (uvicorn)           │
│                                      │
│  ┌─────────────┐  ┌──────────────┐  │
│  │ API Routes  │  │ APScheduler  │  │
│  │ /api/v1/... │  │ (async cron) │  │
│  └─────────────┘  └──────┬───────┘  │
│                          │           │
│            00:00 daily   │           │
│                          ▼           │
│              daily_pipeline()        │
│         Scrape → Snapshot → Retrain  │
└─────────────────────────────────────┘
```

**How it starts:** Automatically when the FastAPI server boots (via `main.py` lifespan).

**Pros:** Zero setup, no Redis/external service needed  
**Cons:** Tied to the web process — if uvicorn restarts, in-flight jobs are lost

### 2. Celery Beat (Production Alternative)

Uses a separate scheduler process with Redis as the message broker.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Celery Beat  │────▶│    Redis     │────▶│Celery Worker │
│ (scheduler)  │     │  (broker)    │     │  (executor)  │
└──────────────┘     └──────────────┘     └──────────────┘
```

**How to start:**

```bash
# Terminal 1: Start the Beat scheduler
celery -A app.tasks.celery_app beat --loglevel=info

# Terminal 2: Start the worker
celery -A app.tasks.celery_app worker --loglevel=info

# Terminal 3: Start the API
uvicorn app.main:app --reload
```

**Pros:** Decoupled from web process, survives API restarts, production-grade  
**Cons:** Requires Redis + 2 extra processes

---

## Key Files

| File | Purpose |
|---|---|
| `app/tasks/scheduler.py` | APScheduler setup, daily pipeline logic, retry mechanism |
| `app/tasks/celery_app.py` | Celery instance + Beat schedule configuration |
| `app/tasks/scrape_task.py` | Celery task wrapper for the chained pipeline |
| `app/tasks/snapshot_task.py` | Standalone Celery task for daily analytics |
| `app/tasks/train_task.py` | Standalone Celery task for ML retraining |
| `app/main.py` | Starts/stops APScheduler in FastAPI lifespan |

---

## API Endpoints

### `GET /api/v1/scrape/schedule`

Check the current scheduler status and next run time.

**Response:**

```json
{
  "scheduler_running": true,
  "timezone": "Asia/Colombo",
  "pipeline": "Scrape (retry ×3) → Snapshot → Retrain",
  "jobs": [
    {
      "id": "daily_pipeline_midnight",
      "name": "Daily Pipeline (Scrape → Snapshot → Retrain)",
      "next_run": "2026-04-16T00:00:00+05:30",
      "trigger": "cron[hour='0', minute='0']"
    }
  ]
}
```

### `POST /api/v1/scrape/trigger/pipeline`

Manually trigger the full daily pipeline (Scrape → Snapshot → Retrain). Runs in background.

**Response:**

```json
{
  "message": "Full daily pipeline started: Scrape → Snapshot → Retrain",
  "status": "running",
  "pipeline_steps": ["scrape (retry ×3)", "snapshot", "retrain"]
}
```

### `GET /api/v1/scrape/status`

Check the result of the last pipeline or scrape run.

**Response (completed):**

```json
{
  "status": "completed",
  "elapsed_seconds": 1842.5,
  "scrape": {
    "status": "completed",
    "total_found": 4523,
    "new_listings": 312,
    "duplicates_skipped": 4211,
    "saved": 312
  },
  "snapshot": {
    "analytics_docs_saved": 225,
    "price_snapshots_saved": 1847
  }
}
```

**Response (failed):**

```json
{
  "status": "failed",
  "stage": "scrape",
  "error": "Scrape failed after 3 attempts. Last error: ConnectionError(...)"
}
```

---

## Logging

All pipeline events are logged with the `⏰` prefix for easy filtering:

```
⏰ DAILY PIPELINE STARTED at 2026-04-16T00:00:00
⏰ Scrape attempt 1/3 started at 2026-04-16T00:00:00
✅ Scrape succeeded on attempt 1/3 in 1523.4s — found=4523 new=312 saved=312
⏰ Daily analytics snapshot started
✅ Daily analytics snapshot complete: {...}
⏰ Model retraining started
✅ Model retraining complete
✅ DAILY PIPELINE COMPLETE in 1842.5s
```

On failure:

```
❌ Scrape attempt 1/3 FAILED: ConnectionError(...)
⏳ Waiting 300s before retry 2/3 …
⏰ Scrape attempt 2/3 started at 2026-04-16T00:05:00
✅ Scrape succeeded on attempt 2/3 in 1480.2s
```

---

## Configuration

### Scheduler Settings (in `scheduler.py`)

| Constant | Default | Description |
|---|---|---|
| `MAX_SCRAPE_RETRIES` | `3` | Max retry attempts for scrape |
| `RETRY_DELAY_SECONDS` | `300` | Seconds between retries (5 min) |
| Trigger time | `00:00` | Cron trigger (midnight) |
| Timezone | `Asia/Colombo` | Sri Lanka Standard Time (UTC+5:30) |
| `misfire_grace_time` | `3600` | Grace period for missed triggers (1 hour) |

### Celery Beat Settings (in `celery_app.py`)

| Setting | Value |
|---|---|
| Broker | Redis (`REDIS_URL` from `.env`) |
| Timezone | `Asia/Colombo` |
| Task serializer | JSON |
| Schedule | `daily_pipeline` at `crontab(hour=0, minute=0)` |

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `APScheduler` | `3.*` | In-process async cron scheduler |
| `celery` | `5.*` | Distributed task queue (optional) |
| `redis` | `5.*` | Celery message broker (optional) |
