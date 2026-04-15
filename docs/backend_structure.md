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
│   ├── main.py                 ← App factory, CORS, router mounting, DB seed
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── listings.py     ← GET /listings, GET /listings/{id}
│   │       ├── analytics.py    ← GET /analytics/avg-price, /trends, /daily, etc.
│   │       ├── deals.py        ← GET /deals/score
│   │       ├── makes.py        ← GET /makes, /makes/{name}/models, /{make}/models/{model}/years
│   │       ├── search.py       ← GET /search
│   │       ├── scrape.py       ← POST /scrape/trigger, /trigger/brand/{b}, /trigger/pipeline, GET /status, /brands, /schedule
│   │       └── logs.py         ← WS /logs/stream
│   ├── core/
│   │   ├── config.py           ← Settings via pydantic-settings (.env)
│   │   ├── database.py         ← MongoDB + Beanie initialisation
│   │   ├── security.py         ← JWT token & API key helpers
│   │   └── logging.py          ← Structured logging setup
│   ├── models/
│   │   ├── listing.py          ← Listing document (make, model, condition strings)
│   │   ├── vehicle.py          ← Make & Model documents (with slug + scrape_url)
│   │   ├── deal_score.py       ← DealScore document
│   │   ├── price_snapshot.py   ← PriceSnapshot (daily make×model×year×condition aggregate)
│   │   └── daily_analytics.py  ← DailyAnalytics document (market/brand/brand_condition)
│   ├── schemas/
│   │   ├── listing.py          ← ListingBase, ListingCreate, ListingResponse
│   │   ├── analytics.py        ← AvgPriceResponse, PriceTrendResponse
│   │   └── deal.py             ← DealScoreResponse
│   ├── scraper/
│   │   ├── brands.py           ← Brand→model registry (53 brands, 546 models + URLs)
│   │   ├── ikman_spider.py     ← Spider — crawl per brand→model→condition
│   │   ├── parser.py           ← HTML parsing (cards + detail pages)
│   │   ├── cleaner.py          ← Data normalisation (price, mileage, year)
│   │   ├── deduplicator.py     ← SHA-256 hash-based duplicate detection
│   │   ├── playwright_fetch.py ← HTTP fetcher (httpx + Playwright fallback)
│   │   ├── storage.py          ← Persist listings to MongoDB
│   │   ├── seeder.py           ← Upsert Make/Model docs from brand registry
│   │   └── runner.py           ← Orchestrates scrape pipeline + daily analytics
│   ├── ml/
│   │   ├── features.py         ← Feature engineering pipeline
│   │   ├── trainer.py          ← Model training logic
│   │   ├── predictor.py        ← Fair price prediction
│   │   ├── scorer.py           ← Deal scoring (good/fair/overpriced)
│   │   └── model_store.py      ← Save/load .pkl model files
│   ├── analytics/
│   │   ├── market_summary.py   ← Aggregate market statistics
│   │   ├── price_trends.py     ← Monthly avg price + year-by-year model history
│   │   ├── depreciation.py     ← Price vs age/mileage curves
│   │   └── daily_snapshot.py   ← Daily analytics engine (4 levels)
│   └── tasks/
│       ├── celery_app.py       ← Celery instance (Redis broker) + Beat schedule
│       ├── scheduler.py        ← APScheduler in-process daily pipeline (Scrape → Snapshot → Retrain)
│       ├── scrape_task.py      ← Celery chained pipeline task (with retry)
│       ├── train_task.py       ← Background ML training task
│       └── snapshot_task.py    ← Daily analytics Celery task
├── models_store/               ← Trained model files (.pkl)
├── tests/                      ← Test suite
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
- **Lifespan**: initialises MongoDB, seeds Make/Model collections, starts APScheduler daily pipeline, and shuts down the scheduler on exit

### `app/core/` — Core Infrastructure

#### `config.py`
- Uses `pydantic-settings` to load all config from `.env`
- Exports a singleton `settings` object
- Key scraper settings: `SCRAPE_MAX_PAGES_PER_BRAND` (default 3), `SCRAPE_DELAY` (1.5s)

#### `database.py`
- Creates an async `AsyncIOMotorClient` connection to MongoDB
- Initialises Beanie ODM with 6 document models:
  `Listing`, `Make`, `Model`, `PriceSnapshot`, `DealScore`, `DailyAnalytics`

---

### `app/models/` — Database Documents (Beanie)

#### `Listing`
- **Collection**: `listings`
- **Indexes**: `source_url`, `source_hash`, `make`, `model`, `condition`, `year`, `posted_date`, compound `[make, model, year, condition]`, `[make, condition]`, `[posted_date, make]`
- **Fields**: title, description, price, currency, mileage, year, location, source_url, source_hash, make, model, condition, category, posted_date, created_at, updated_at

#### `Make`
- **Collection**: `makes`
- **Indexes**: `name`, `slug`
- **Fields**: name, slug, scrape_url

#### `Model`
- **Collection**: `models`
- **Indexes**: `name`, `slug`, `make_slug`, compound `[make_slug, slug]`
- **Fields**: name, slug, make_slug, scrape_url

#### `DealScore`
- **Collection**: `deal_scores`
- **Indexes**: `listing_id`
- **Fields**: listing_id, predicted_price, actual_price, score, label, scored_at

#### `PriceSnapshot`
- **Collection**: `price_snapshots`
- **Indexes**: compound `[snapshot_date, make, model, year, condition]`, `[make, model]`
- **Fields**: snapshot_date, make, model, year, condition, avg_price, min_price, max_price, listing_count, captured_at
- **Note**: Each document is a **daily aggregate** for one make×model×year×condition group, not per-listing

#### `DailyAnalytics`
- **Collection**: `daily_analytics`
- **Indexes**: compound `[snapshot_date, scope, brand, condition]`
- **Fields**: snapshot_date, scope, brand, condition, total_listings, avg_price, min_price, max_price, median_price, price_change_pct, created_at

---

### `app/scraper/` — Web Scraping Pipeline

The scraper crawls ikman.lk at model-level granularity:

```
For brands WITH model data (53 brands, 546 models):
  brand → model → condition → pages
  e.g. toyota/aqua?tree.brand=toyota_toyota-aqua&enum.condition=used

For brands WITHOUT model data (3 brands):
  brand → condition → pages (brand-level fallback)
```

#### Pipeline:

```
1. Crawl (ikman_spider.py)
   ↓ brand → model → condition (make/model injected from URL context)
2. Parse (parser.py)
   ↓ extract structured data from HTML
3. Clean (cleaner.py)
   ↓ normalise price, mileage, year
4. Deduplicate (deduplicator.py)
   ↓ filter existing records by source_hash
5. Store (storage.py)
   ↓ persist to MongoDB
6. Analyse (daily_snapshot.py)
   ↓ compute daily analytics + price snapshot aggregates
```

#### `brands.py`
- Complete brand→model registry for 53 brands (546 models)
- URL builder: `build_model_url(brand, model_slug, condition, page)`
- Remaining 3 brands use `build_brand_url()` (brand-level only)

#### `ikman_spider.py`
- `crawl_model()` — crawl one brand+model+condition combo
- `crawl_brand()` — crawl all models for a brand
- `crawl_all_brands()` — full market sweep
- Make, model, condition always injected from URL context (never null for registered brands)

#### `seeder.py`
- `seed_makes_and_models()` — upserts all Make/Model docs from brand registry
- Runs automatically on server startup via `main.py` lifespan
- Stores `scrape_url` for every make and model

#### `runner.py`
- `run_scrape_cycle()` — orchestrates: crawl → dedup → store → daily analytics
- `run_brand_scrape(brand)` — single-brand convenience wrapper

---

### `app/analytics/` — Market Analytics

#### `market_summary.py`
- `market_summary()` — aggregate stats: total listings, avg price, makes/models count

#### `price_trends.py`
- `monthly_avg_price(make, model, months)` — monthly avg price from listings
- `model_year_price_history(make, model, condition)` — year-by-year avg from PriceSnapshot aggregates

#### `depreciation.py`
- `depreciation_curve(make, model)` — price vs manufacturing year
- `mileage_curve(make, model)` — price vs mileage bands (25k km buckets)

#### `daily_snapshot.py`
- `compute_and_save_daily_analytics()` — produces snapshots at 4 levels:
  1. **Market-wide** — 1 DailyAnalytics doc/day
  2. **Per-brand** — ~56 DailyAnalytics docs/day
  3. **Per-brand×condition** — ~168 DailyAnalytics docs/day
  4. **Per-make×model×year×condition** — PriceSnapshot records for granular trend analysis
- **Features**: Applies IQR-based outlier filtering and `posted_date` matching for true day-by-day analysis.

---

### `app/tasks/` — Scheduling & Background Tasks

Supports two scheduling engines:

#### `scheduler.py` — APScheduler (In-Process, Default)
- Runs inside the FastAPI process — **no extra services needed**
- **Daily pipeline** triggered at midnight: Scrape (with retry ×3) → Snapshot → Retrain
- Each step only runs after the previous one succeeds
- Scrape retries up to 3 times with 5-minute delays between attempts
- Started/stopped automatically via `main.py` lifespan

#### `celery_app.py` — Celery Beat (Production Alternative)
- Requires **Redis** as message broker + separate Beat/Worker processes
- Single `daily_pipeline` task scheduled at `crontab(hour=0, minute=0)`
- Task name: `daily_pipeline` (chained: scrape → snapshot → retrain)

#### `scrape_task.py`
- **Task name**: `daily_pipeline` — Celery chained pipeline with built-in retry
- Also exports standalone `scrape_listings` task for manual triggers

#### `snapshot_task.py`
- **Task name**: `snapshot_prices`
- Calls `compute_and_save_daily_analytics()` to generate all snapshots

**Running the Celery worker:**

```bash
# Terminal 1: Scheduler
celery -A app.tasks.celery_app beat --loglevel=info

# Terminal 2: Worker
celery -A app.tasks.celery_app worker --loglevel=info
```

> **See also:** [Scheduler Documentation](scheduler.md) for full pipeline details, retry logic, and architecture.

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        ikman.lk                               │
│   56 brands × 546 models × 3 conditions                       │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP (httpx / Playwright)
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  Scraper Pipeline                                             │
│  Spider → Parser → Cleaner → Dedup → Store → Analytics       │
└──────────────────────────────────────────────────────┬───────┘
                                                       ▼
┌──────────────────────────────────────────────────────────────┐
│  MongoDB                                                      │
│  ┌──────────┐ ┌─────┐ ┌──────┐ ┌───────────┐ ┌───────────┐ │
│  │ listings │ │makes│ │models│ │deal_scores│ │price_snaps│ │
│  └──────────┘ └─────┘ └──────┘ └───────────┘ └───────────┘ │
│  ┌─────────────────┐                                         │
│  │ daily_analytics │                                         │
│  └─────────────────┘                                         │
└────────────────────────┬─────────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  FastAPI  /api/v1/                                            │
│  listings  analytics  deals  makes  search  scrape            │
└──────────────────────────────────────────────────────────────┘
```

---

## Development Status

| Module | Status | Notes |
|---|---|---|
| API Routes | ✅ Complete | All 24 endpoints connected to MongoDB |
| Models | ✅ Complete | 6 Beanie documents with compound indexes |
| Schemas | ✅ Complete | Pydantic schemas match current models |
| Scraper | ✅ Functional | Model-level crawling for 53 brands, brand-level for 3 |
| Analytics | ✅ Functional | 4-level daily snapshots, depreciation, mileage curves |
| ML | 🔧 Scaffolded | Scorer logic complete, trainer/predictor need implementation |
| Scheduler | ✅ Functional | Daily chained pipeline (Scrape→Snapshot→Retrain) with retry |
| Tasks | ✅ Functional | APScheduler (default) + Celery Beat (optional) |
| Security | 🔧 Scaffolded | JWT & API key helpers stubbed |
