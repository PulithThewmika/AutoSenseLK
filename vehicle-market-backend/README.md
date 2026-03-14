# Vehicle Market Backend

> FastAPI-powered backend for scraping, analysing, and scoring Sri Lankan vehicle listings.

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Database | PostgreSQL + SQLAlchemy (async) |
| Migrations | Alembic |
| Queue | Celery + Redis |
| Scraping | Scrapy + Playwright |
| ML | scikit-learn + pandas |
| Containers | Docker + Docker Compose |

## Quick Start

```bash
# 1. Clone and enter the directory
cd vehicle-market-backend

# 2. Copy environment variables
cp .env.example .env

# 3. Start all services
docker compose up --build

# 4. API is now live at http://localhost:8000
#    Docs at http://localhost:8000/docs
```

## Project Structure

```
app/
├── api/          # FastAPI routes & dependencies
│   └── v1/       # Versioned endpoints
├── core/         # Config, DB, security, logging
├── models/       # SQLAlchemy ORM models
├── schemas/      # Pydantic request / response schemas
├── scraper/      # Web scraping pipeline
├── ml/           # Machine-learning training & prediction
├── analytics/    # Market analytics & trends
├── tasks/        # Celery background tasks
└── main.py       # App factory & router mount
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/listings` | Paginated listings with filters |
| GET | `/api/v1/listings/{id}` | Single listing detail |
| GET | `/api/v1/analytics/avg-price` | Average price by make/model |
| GET | `/api/v1/analytics/trends` | Monthly price trends |
| GET | `/api/v1/deals/score?listing_id=` | Deal quality score |
| GET | `/api/v1/makes` | All vehicle makes |
| GET | `/api/v1/makes/{id}/models` | Models for a make |
| GET | `/api/v1/search?q=` | Full-text search |

## Development

```bash
# Run locally without Docker
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## License

Private — All rights reserved.
