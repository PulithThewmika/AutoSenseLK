# Backend Structure

> **Location**: `vehicle-market-backend/`  
> **Framework**: FastAPI + Uvicorn  
> **Database**: MongoDB (Motor + Beanie ODM)  
> **Entry Point**: `uvicorn app.main:app --reload`

---

## Directory Layout

```
vehicle-market-backend/
├── app/
│   ├── main.py                 ← App factory, CORS, router mounting
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── listings.py     ← GET /listings, GET /listings/{id}
│   │       ├── analytics.py    ← GET /analytics/avg-price, /trends
│   │       ├── deals.py        ← GET /deals/score
│   │       ├── makes.py        ← GET /makes, GET /makes/{id}/models
│   │       ├── search.py       ← GET /search
│   │       └── scrape.py       ← POST /scrape/trigger, POST /scrape/trigger/brand/{brand}, GET /scrape/status
│   ├── core/
│   │   ├── config.py           ← Settings via pydantic-settings (.env)
│   │   ├── database.py         ← MongoDB + Beanie initialisation
│   │   ├── security.py         ← JWT token & API key helpers
│   │   └── logging.py          ← Structured logging setup
│   ├── models/
│   │   ├── listing.py          ← Listing document
│   │   ├── vehicle.py          ← Make & Model documents
│   │   ├── deal_score.py       ← DealScore document
│   │   ├── price_snapshot.py   ← PriceSnapshot document
│   │   └── daily_analytics.py  ← DailyAnalytics document
│   ├── schemas/
│   │   ├── listing.py          ← ListingBase, ListingCreate, ListingResponse
│   │   ├── analytics.py        ← AvgPriceResponse, PriceTrendResponse
│   │   └── deal.py             ← DealScoreResponse
│   ├── scraper/
│   │   ├── brands.py           ← Registry of 55+ brands & config
│   │   ├── ikman_spider.py     ← Main spider — crawl + parse + clean
│   │   ├── parser.py           ← HTML parsing (cards + detail pages)
│   │   ├── cleaner.py          ← Data normalisation (price, mileage, year)
│   │   ├── deduplicator.py     ← SHA-256 hash-based duplicate detection
│   │   ├── playwright_fetch.py ← HTTP fetcher (httpx + Playwright fallback)
│   │   ├── storage.py          ← Persist listings to MongoDB
│   │   └── runner.py           ← Orchestrates the full scrape pipeline
│   ├── ml/
│   │   ├── features.py         ← Feature engineering pipeline
│   │   ├── trainer.py          ← Model training logic
│   │   ├── predictor.py        ← Fair price prediction
│   │   ├── scorer.py           ← Deal scoring (good/fair/overpriced)
│   │   └── model_store.py      ← Save/load .pkl model files
│   ├── analytics/
│   │   ├── market_summary.py   ← Aggregate market statistics
│   │   ├── price_trends.py     ← Monthly average price computation
│   │   ├── depreciation.py     ← Price vs age/mileage curves
│   │   └── daily_snapshot.py   ← Engine for market/brand daily snapshots
│   └── tasks/
│       ├── celery_app.py       ← Celery instance (Redis broker)
│       ├── scrape_task.py      ← Background scrape task
│       ├── train_task.py       ← Background ML training task
│       └── snapshot_task.py    ← Daily price snapshot task
├── models_store/               ← Trained model files (.pkl)
├── tests/                      ← Test suite
├── alembic/                    ← Database migrations (historical)
├── requirements.txt            ← Python dependencies
├── .env                        ← Environment configuration
└── .env.example                ← Template for .env
```

---

## Module Details

### `app/main.py` — Application Factory

- Creates the FastAPI app with metadata (title, version, description)
- Configures CORS middleware (allows all origins in dev)
- Mounts all v1 routers under `/api/v1`
- Registers a `/health` endpoint
- Uses a **lifespan** context manager to initialise MongoDB on startup

### `app/core/` — Core Infrastructure

#### `config.py`
- Uses `pydantic-settings` to load all config from `.env`
- Exports a singleton `settings` object used throughout the app
- Groups: App, MongoDB, Redis/Celery, Security, Scraper settings

#### `database.py`
- Creates an async `AsyncIOMotorClient` connection to MongoDB
- Initialises Beanie ODM with all 6 document models:
  `Listing`, `Make`, `Model`, `PriceSnapshot`, `DealScore`, `DailyAnalytics`

#### `security.py`
- `create_access_token()` — Generate signed JWT tokens
- `verify_api_key()` — Validate API keys
- Currently stubbed with `...` (implementation pending)

#### `logging.py`
- Configures structured logging to stdout
- Format: `timestamp | LEVEL | logger_name | message`
- Exports a `logger` instance named `vehicle_market`

---

### `app/models/` — Database Documents (Beanie)

All models extend Beanie's `Document` class and map to MongoDB collections.

#### `Listing`
- **Collection**: `listings`
- **Indexes**: `source_url`, `source_hash`, `make_id`, `model_id`
- **Fields**: title, description, price, currency, mileage, year, location, source_url, source_hash, category, transmission, fuel_type, engine_capacity, condition, seller_name, image_urls, created_at, updated_at

#### `Make`
- **Collection**: `makes`
- **Indexes**: `name`
- **Fields**: name

#### `Model`
- **Collection**: `models`
- **Indexes**: `name`, `make_id`
- **Fields**: name, make_id (reference to Make)

#### `DealScore`
- **Collection**: `deal_scores`
- **Indexes**: `listing_id`
- **Fields**: listing_id, predicted_price, actual_price, score, label, scored_at

#### `PriceSnapshot`
- **Collection**: `price_snapshots`
- **Indexes**: `listing_id`, `captured_at`
- **Fields**: listing_id, price, captured_at

#### `DailyAnalytics`
- **Collection**: `daily_analytics`
- **Indexes**: `snapshot_date`, `scope`, `brand`, `condition` (compound)
- **Fields**: snapshot_date, scope, brand, condition, total_listings, avg_price, min_price, max_price, median_price, price_change_pct, created_at

---

### `app/scraper/` — Web Scraping Pipeline

The scraper follows a 5-step pipeline orchestrated by `runner.py`:

```
1. Crawl (ikman_spider.py)
   ↓ 55 brands × 3 conditions
2. Parse (parser.py)
   ↓ extract structured data
3. Clean (cleaner.py)
   ↓ normalise values
4. Deduplicate (deduplicator.py)
   ↓ filter existing records
5. Store & Analyze (storage.py, daily_snapshot.py)
   ↓ persist to MongoDB & compute daily analytics
```

#### `brands.py`
- Registry of 55+ vehicle brands in Sri Lanka
- Defines condition mappings (`used`, `brand_new`, `reconditioned`)
- Generates specific URLs for combinations (e.g. Toyota Used)

#### `ikman_spider.py`
- Follows brand-specific URLs (brand + condition filters)
- Iterates through configurable number of pages per brand (`SCRAPE_MAX_PAGES_PER_BRAND`)
- Optionally fetches individual detail pages for richer data
- Applies cleaning to all listings before returning

#### `parser.py`
- **`parse_listing_cards(html)`** — Extracts ads from index pages
  - Parses title, price, mileage, location, category from card elements
  - Detects Sri Lankan districts (25 districts) and vehicle categories
- **`parse_listing_detail(html)`** — Extracts rich data from ad detail pages
  - Make, model, year, condition, transmission, fuel type, engine capacity
  - Description, images, location
  - Uses multiple CSS selector strategies for robustness

#### `cleaner.py`
- **`clean_price()`** — Normalises `"Rs 7,800,000"` → `7800000.0`
- **`clean_mileage()`** — Normalises km/miles → kilometres
- **`clean_year()`** — Extracts 4-digit year from various formats
- **`clean_listing()`** — Applies all cleaning to a raw dict

#### `deduplicator.py`
- Generates SHA-256 hash from `source_url + title + price`
- Checks against existing `source_hash` values in MongoDB
- Returns `(new_listings, skipped_count)` tuple

#### `playwright_fetch.py`
- Primary: `httpx` async HTTP client (fast, lightweight)
- Fallback: Playwright headless Chromium (for JS-rendered pages)
- Implements retry logic with exponential backoff (3 retries)
- Polite sequential fetching with configurable delay

#### `storage.py`
- Upsert logic: updates existing listings (by `source_hash`) or inserts new ones
- Preserves `created_at` on updates, sets `updated_at`

#### `runner.py`
- `run_scrape_cycle()` — Async orchestrator for the full pipeline
- `run_scrape_cycle_sync()` — Synchronous wrapper for Celery tasks

---

### `app/ml/` — Machine Learning Module

#### `features.py`
- `build_features(listing)` — Transforms raw listing dict into a feature vector
- Planned: encode make/model, normalise year, mileage, etc.

#### `trainer.py`
- `train_model()` — Train/retrain the price-prediction regression model
- Planned: load data → feature engineering → train → evaluate → save

#### `predictor.py`
- `predict_price(features)` — Returns the predicted fair market price

#### `scorer.py`
- `score_listing(predicted, actual)` — Computes deal quality
- Thresholds: < 0.85 = `good_deal`, 0.85–1.15 = `fair`, > 1.15 = `overpriced`

#### `model_store.py`
- `save_model(model, name)` — Pickle-serialise model to `models_store/`
- `load_model(name)` — Load a saved model from disk

---

### `app/analytics/` — Market Analytics

#### `market_summary.py`
- `market_summary()` — Aggregate stats: total listings, avg price, makes/models count

#### `price_trends.py`
- `monthly_avg_price(make, model, months)` — Monthly avg price over time

#### `depreciation.py`
- `depreciation_curve(make, model)` — Price vs year data points
- `mileage_curve(make, model)` — Price vs mileage data points

#### `daily_snapshot.py`
- `compute_and_save_daily_analytics()` — Aggregates the listing collection into a daily snapshot
- Computes overall market-wide analytics, per-brand, and per-brand×condition stats
- Stores min, max, average, and median pricing along with % changes


---

### `app/tasks/` — Celery Background Tasks

Requires **Redis** as message broker.

#### `celery_app.py`
- Creates `Celery` instance with Redis broker/backend
- Config: JSON serialisation, `Asia/Colombo` timezone, UTC enabled

#### `scrape_task.py`
- **Task name**: `scrape_listings`
- Calls `run_scrape_cycle_sync()` to run a full scrape

#### `train_task.py`
- **Task name**: `retrain_model`
- Calls `train_model()` to retrain the ML model

#### `snapshot_task.py`
- **Task name**: `snapshot_prices`
- Archives current prices of all active listings

**Running the Celery worker:**

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        ikman.lk                               │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP (httpx / Playwright)
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  Scraper Pipeline                                             │
│  ┌─────────┐  ┌────────┐  ┌─────────┐  ┌──────┐  ┌───────┐ │
│  │ Spider  │→│ Parser │→│ Cleaner │→│ Dedup │→│ Store │  │
│  └─────────┘  └────────┘  └─────────┘  └──────┘  └───┬───┘ │
└──────────────────────────────────────────────────────┬───────┘
                                                       │
                                                       ▼
┌──────────────────────────────────────────────────────────────┐
│  MongoDB                                                      │
│  ┌───────────┐ ┌──────┐ ┌────────┐ ┌───────────┐ ┌────────┐│
│  │ listings  │ │makes │ │models  │ │deal_scores│ │snapshots││
│  └───────────┘ └──────┘ └────────┘ └───────────┘ └────────┘│
│  ┌─────────────────┐                                       │
│  │ daily_analytics │                                       │
│  └─────────────────┘                                       │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  FastAPI                                                      │
│  /api/v1/listings  /analytics  /deals  /makes  /search       │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  React Frontend (localhost:5173)                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Development Status

| Module | Status | Notes |
|---|---|---|
| API Routes | ✅ Scaffolded | Endpoints return placeholder data, DB queries pending |
| Models | ✅ Complete | All Beanie documents defined with indexes |
| Schemas | ✅ Complete | Pydantic models for all endpoints |
| Scraper | ✅ Functional | Full pipeline: fetch → parse → clean → dedup → store |
| ML | 🔧 Scaffolded | Scorer logic complete, trainer/predictor need implementation |
| Analytics | 🔧 Scaffolded | Functions defined, DB queries pending |
| Tasks | ✅ Scaffolded | Celery tasks defined, require Redis to run |
| Security | 🔧 Scaffolded | JWT & API key helpers stubbed |
