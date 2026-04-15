# AutoSenseLK — Technical Reference

> Complete technical documentation for the AutoSenseLK vehicle market intelligence platform. For a high-level overview, see the [README](../README.md).

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         ikman.lk                                  │
│   55 brands × 300+ models × 3 conditions                         │
└────────────────────────┬─────────────────────────────────────────┘
                         │ httpx / Playwright
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│  Scraper Pipeline                                                  │
│  Spider → Parser → Cleaner → Dedup → Storage → Analytics         │
└──────────────────────────────────────────────────────┬───────────┘
                                                        │
                                                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  MongoDB collections                                              │
│  listings  makes  models  price_snapshots  daily_analytics        │
│  deal_scores                                                      │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│  FastAPI  (localhost:8000)                                        │
│  /listings  /analytics  /makes  /deals  /search  /scrape         │
└────────────────────────┬─────────────────────────────────────────┘
                         │ HTTP
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│  React Frontend  (localhost:5173)                                 │
│  Market Dashboard · Brand Explorer · Deal Finder                 │
└──────────────────────────────────────────────────────────────────┘
```

**Optional async layer:**

```
FastAPI ──► Celery Worker ──► Redis
           (Scrape / Analytics / ML training tasks)
```

---

## Tech Stack

### Backend

| Layer | Technology |
|---|---|
| API framework | FastAPI 0.115 + Uvicorn |
| Database | MongoDB 6+ via Motor (async driver) |
| ODM | Beanie 1.x |
| Task queue | Celery 5 + Redis |
| Scraping | httpx + Playwright + BeautifulSoup + lxml |
| ML | scikit-learn + pandas + NumPy |
| Auth | python-jose (JWT) + passlib (bcrypt) |
| Config | pydantic-settings + python-dotenv |

### Frontend

| Layer | Technology |
|---|---|
| Framework | React 19 + TypeScript |
| Build tool | Vite 8 |
| Charts | Chart.js + react-chartjs-2 |
| Fonts | Google Fonts (Syne, DM Sans, DM Mono) |
| Linting | ESLint + typescript-eslint |

---

## Project Structure

```
AutoSenseLK/
├── docs/                              ← Detailed documentation
│   ├── project_overview.md
│   ├── api_documentation.md
│   ├── backend_structure.md
│   ├── frontend_structure.md
│   ├── scheduler.md
│   └── technical_reference.md         ← This file
│
├── vehicle-market-backend/            ← FastAPI application
│   ├── app/
│   │   ├── main.py                   ← App factory + startup seeder
│   │   ├── api/v1/                   ← REST endpoints
│   │   │   ├── listings.py
│   │   │   ├── analytics.py
│   │   │   ├── deals.py
│   │   │   ├── makes.py
│   │   │   ├── search.py
│   │   │   └── scrape.py
│   │   ├── core/                     ← Config, DB, security, logging
│   │   ├── models/                   ← Beanie MongoDB documents
│   │   │   ├── listing.py
│   │   │   ├── vehicle.py            ← Make & Model
│   │   │   ├── price_snapshot.py
│   │   │   ├── daily_analytics.py
│   │   │   └── deal_score.py
│   │   ├── schemas/                  ← Pydantic request/response types
│   │   ├── scraper/
│   │   │   ├── brands.py             ← 300+ model registry + URL builder
│   │   │   ├── ikman_spider.py       ← Main spider
│   │   │   ├── parser.py
│   │   │   ├── cleaner.py
│   │   │   ├── deduplicator.py
│   │   │   ├── playwright_fetch.py
│   │   │   ├── storage.py
│   │   │   ├── seeder.py             ← Auto-seeds Make/Model on startup
│   │   │   └── runner.py
│   │   ├── analytics/
│   │   │   ├── daily_snapshot.py     ← 4-level daily analytics engine
│   │   │   ├── price_trends.py
│   │   │   ├── depreciation.py
│   │   │   └── market_summary.py
│   │   ├── ml/
│   │   │   ├── scorer.py
│   │   │   ├── predictor.py
│   │   │   ├── trainer.py
│   │   │   ├── features.py
│   │   │   └── model_store.py
│   │   └── tasks/                    ← Celery background tasks
│   ├── models_store/                 ← Trained ML .pkl files
│   ├── .env.example
│   └── requirements.txt
│
├── vehicle-market-frontend/
│   └── AutoSenseLK/                  ← Vite + React app
│       └── src/
│           ├── App.tsx
│           ├── components/
│           └── index.css
│
└── vehicle-market-admindash/         ← Admin Dashboard (Vite + React)
```

---

## Quick Start

### Prerequisites

| Tool | Version | Required? |
|---|---|---|
| Python | 3.10+ | ✅ Yes |
| Node.js | 18+ | ✅ Yes |
| MongoDB | 6.0+ | ✅ Yes |
| Redis | 7.0+ | ❌ Optional (background tasks only) |

---

### 1 — Backend

```bash
cd vehicle-market-backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser (for JS-heavy pages)
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env — set MONGODB_URL and any other values

# Start the API server
uvicorn app.main:app --reload
```

The server starts at **http://localhost:8000**

On startup it will:
1. Connect to MongoDB
2. Seed the `makes` and `models` collections from the brand registry

---

### 2 — Frontend

```bash
cd vehicle-market-frontend/AutoSenseLK
npm install
npm run dev
```

Frontend runs at **http://localhost:5173**

---

### 3 — Trigger a scrape

```bash
# Full market scrape (all brands, all models, all conditions)
curl -X POST http://localhost:8000/api/v1/scrape/trigger

# Single-brand scrape
curl -X POST http://localhost:8000/api/v1/scrape/trigger/brand/toyota
```

---

### 4 — Docker (all services)

```bash
cd vehicle-market-backend
docker compose up --build
```

---

## Environment Variables

Create `vehicle-market-backend/.env` from `.env.example`:

| Variable | Default | Description |
|---|---|---|
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGODB_DB_NAME` | `vehicle_market` | Database name |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis URL (Celery broker) |
| `API_KEY` | *(empty)* | API key for protected endpoints |
| `JWT_SECRET` | `change-me` | JWT signing secret |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `SCRAPE_BASE_URL` | `https://ikman.lk` | Scrape target |
| `SCRAPE_MAX_PAGES_PER_BRAND` | `3` | Pages crawled per brand×model×condition |
| `SCRAPE_DELAY` | `1.5` | Seconds between requests |
| `DEBUG` | `False` | Enable debug mode |

---

## API Overview

Interactive docs: **http://localhost:8000/docs**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/listings/` | Paginated listings (filter by make, model, price, year) |
| `GET` | `/api/v1/listings/{id}` | Single listing detail |
| `GET` | `/api/v1/analytics/avg-price` | Average price by make/model |
| `GET` | `/api/v1/analytics/trends` | Monthly price trends |
| `GET` | `/api/v1/analytics/summary` | Market-wide statistics |
| `GET` | `/api/v1/analytics/depreciation` | Price depreciation curve |
| `GET` | `/api/v1/analytics/mileage` | Price vs mileage curve |
| `GET` | `/api/v1/analytics/daily` | Latest market snapshot |
| `GET` | `/api/v1/analytics/daily/brands` | Latest snapshot for all brands |
| `GET` | `/api/v1/analytics/daily/brand/{brand}` | Brand snapshot with condition breakdown |
| `GET` | `/api/v1/analytics/daily/history` | Historical daily snapshots |
| `GET` | `/api/v1/deals/score` | Deal quality score for a listing |
| `GET` | `/api/v1/makes/` | All makes with scrape URLs |
| `GET` | `/api/v1/makes/{name}/models` | Models for a make with listing counts |
| `GET` | `/api/v1/makes/{make}/models/{model}/years` | Year-by-year price history |
| `GET` | `/api/v1/search/` | Full-text listing search |
| `POST` | `/api/v1/scrape/trigger` | Trigger full market scrape |
| `POST` | `/api/v1/scrape/trigger/brand/{brand}` | Trigger single-brand scrape |
| `GET` | `/api/v1/scrape/status` | Last scrape result |
| `GET` | `/api/v1/scrape/brands` | Supported brands list |

> Full request/response schemas: [`docs/api_documentation.md`](api_documentation.md)

---

## Scraper

The scraper follows a **brand → model → condition** crawl strategy using model-specific ikman.lk URLs:

```
https://ikman.lk/en/ads/sri-lanka/cars/{brand}/{model}?tree.brand={brand}_{brand}-{model}&enum.condition={condition}
```

### Supported brands with model-level crawling

| Brand | Models |
|---|---|
| Toyota | 68 models (Aqua, Prius, Vezel, Axio, Hilux…) |
| Honda | 26 models (Vezel, CRV, Fit, Civic, City…) |
| Suzuki | 28 models (Alto, Wagon R, Swift, Spacia…) |
| Nissan | 35 models (Sunny, X-Trail, March, Leaf…) |
| Mercedes-Benz | 47 models (C200, E200, GLB, G Wagon…) |
| Mitsubishi | 23 models (Lancer, Montero, Outlander…) |
| Land Rover | 9 models (Defender, Range Rover, Discovery…) |
| Daihatsu | 17 models (Mira, Rocky, Taft, Boon…) |
| Audi | 13 models (A3, Q3, Q5, A4, e-tron…) |
| BMW | 50 models (X1, X3, X5, 318i, i3…) |
| Kia | 17 models (Sonet, Sorento, Sportage…) |

An additional 44 brands (Micro, DFS, Hyundai, Ford, etc.) are scraped at brand level.

### Pipeline

```
Crawl → Parse → Clean → Deduplicate → Store → Analyse
```

1. **Crawl** — fetches listing pages (httpx, falls back to Playwright for JS-rendered content)
2. **Parse** — extracts title, price, mileage, location from index cards; `make`, `model`, `condition` are injected from URL context
3. **Clean** — normalises price (`"Rs 7,800,000"` → `7800000.0`), mileage (miles → km), year
4. **Deduplicate** — SHA-256 hash of `source_url + title + price` prevents re-inserting existing listings
5. **Store** — upserts into `listings` collection
6. **Analyse** — triggers `compute_and_save_daily_analytics()` after every cycle

---

## Analytics Engine

### 4-level daily aggregation

Every scrape cycle computes analytics at four levels of granularity:

| Level | Documents/day | Key use |
|---|---|---|
| Market-wide | 1 | Overall market health |
| Per-brand | ~55 | Brand comparison |
| Per-brand × condition | ~165 | New vs used vs reconditioned |
| Per-make × model × year × condition | Thousands | Clean depreciation tracking via `PriceSnapshot` |

### Key functions

- `compute_and_save_daily_analytics()` — full 4-level engine
- `model_year_price_history(make, model, condition)` — queries `PriceSnapshot` aggregates for year-by-year pricing without recalculating from raw listings
- `depreciation_curve(make, model)` — price vs manufacturing year
- `mileage_curve(make, model)` — price vs mileage in 25k km buckets
- `monthly_avg_price(make, model, months)` — month-by-month trend

---

## Machine Learning — Deal Scoring

The deal scorer compares a listing's asking price against the average price for the same make and model:

| Label | Ratio (actual ÷ predicted) | Meaning |
|---|---|---|
| `good_deal` | < 0.85 | Listed >15% below market average |
| `fair` | 0.85 – 1.15 | Within ±15% of market |
| `overpriced` | > 1.15 | Listed >15% above market average |

Access via `GET /api/v1/deals/score?listing_id={id}`

> A full regression model (scikit-learn) is scaffolded in `app/ml/` for future training on richer feature sets.

---

## Database Schema

### `listings`

| Field | Type | Description |
|---|---|---|
| `make` | string | Vehicle make (e.g. "Toyota") |
| `model` | string | Vehicle model (e.g. "Aqua") |
| `condition` | string | `used` / `brand_new` / `reconditioned` |
| `price` | float | Price in LKR |
| `year` | int | Manufacturing year |
| `mileage` | float | Mileage in km |
| `location` | string | Sri Lankan district |
| `source_url` | string | Original ikman.lk URL |
| `source_hash` | string | SHA-256 dedup key |

**Indexes**: `source_hash` (unique), `[make, model, year, condition]` (analytics)

### `makes` / `models`

Both documents store `name`, `slug`, and `scrape_url`. Seeded automatically on server startup from the brand registry.

### `price_snapshots`

Daily aggregate per `make × model × year × condition` group. Stores `avg_price`, `min_price`, `max_price`, `listing_count`.

### `daily_analytics`

Daily aggregate at market / brand / brand×condition scope. Stores `avg_price`, `min_price`, `max_price`, `median_price`, `total_listings`, `price_change_pct`.

---

## Background Tasks

Tasks run via **Celery** with **Redis** as the broker:

```bash
# Start the Celery worker
celery -A app.tasks.celery_app worker --loglevel=info
```

| Task name | Trigger | What it does |
|---|---|---|
| `scrape_listings` | Manual / scheduled | Full market scrape cycle |
| `snapshot_prices` | Post-scrape / scheduled | Runs `compute_and_save_daily_analytics()` |
| `retrain_model` | Manual / scheduled | Retrains the ML pricing model |

> Redis is **optional** for development. Scrape and analytics can be triggered directly via `POST /api/v1/scrape/trigger` without a Celery worker.

---

## Development

### Running tests

```bash
cd vehicle-market-backend
pytest tests/ -v
```

### Verifying imports

```bash
python -c "import app.main; print('OK')"
```

### Useful endpoints during development

```bash
# Check health
curl http://localhost:8000/health

# Trigger model-level scrape for Toyota
curl -X POST http://localhost:8000/api/v1/scrape/trigger/brand/toyota

# Check scrape result
curl http://localhost:8000/api/v1/scrape/status

# Get Toyota Aqua average price
curl "http://localhost:8000/api/v1/analytics/avg-price?make=Toyota&model=Aqua"

# Year-by-year Aqua price history
curl "http://localhost:8000/api/v1/makes/toyota/models/aqua/years"
```

---

## Related Documentation

| Document | Description |
|---|---|
| [`project_overview.md`](project_overview.md) | Full tech stack, quick start, env vars, service dependencies |
| [`api_documentation.md`](api_documentation.md) | All 22 endpoints with request/response schemas |
| [`backend_structure.md`](backend_structure.md) | Module-by-module backend architecture |
| [`frontend_structure.md`](frontend_structure.md) | React component structure and API integration |
| [`scheduler.md`](scheduler.md) | Daily pipeline, retry logic, architecture |
