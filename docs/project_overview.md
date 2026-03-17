# AutoSenseLK — Project Overview

> A data-driven platform that monitors Sri Lankan vehicle market prices by collecting and analysing listing data from ikman.lk. The system provides market insights, price trends, deal scoring, and average price analytics to help users make better buying and selling decisions.

---

## Tech Stack

### Backend

| Layer | Technology | Purpose |
|---|---|---|
| **API Framework** | FastAPI + Uvicorn | Async REST API |
| **Database** | MongoDB (Motor async driver) | Document storage for listings |
| **ODM** | Beanie | MongoDB object-document mapper |
| **Task Queue** | Celery + Redis | Background job processing |
| **Scraping** | httpx + Playwright + BeautifulSoup + lxml | Data collection from ikman.lk |
| **ML** | scikit-learn + pandas + NumPy | Price prediction & deal scoring |
| **Security** | python-jose (JWT) + passlib (bcrypt) | Authentication & API key validation |
| **Config** | pydantic-settings + python-dotenv | Environment-based configuration |

### Frontend

| Layer | Technology | Purpose |
|---|---|---|
| **Framework** | React 19 + TypeScript | UI components |
| **Build Tool** | Vite 8 | Dev server & bundler |
| **Charting** | Chart.js + react-chartjs-2 | Price trend visualisations |
| **Fonts** | Google Fonts (Syne, DM Sans, DM Mono) | Typography |
| **Linting** | ESLint + typescript-eslint | Code quality |

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| MongoDB | 6.0+ | Primary database (must be running) |
| Redis | 7.0+ | **Optional** — only for Celery background tasks |
| Docker | (optional) | Alternative to local installs |

---

## Quick Start

### 1. Backend

```bash
cd vehicle-market-backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URL, Redis URL, secrets, etc.

# Start the API
uvicorn app.main:app --reload
```

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Frontend

```bash
cd vehicle-market-frontend/AutoSenseLK

# Install dependencies
npm install

# Start dev server
npm run dev
```

- **App**: http://localhost:5173

### 3. Docker (All Services)

```bash
cd vehicle-market-backend
docker compose up --build
```

---

## Environment Variables

All configuration is loaded from `vehicle-market-backend/.env`:

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Vehicle Market API` | Application display name |
| `APP_VERSION` | `0.1.0` | API version string |
| `DEBUG` | `False` | Debug mode toggle |
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGODB_DB_NAME` | `vehicle_market` | Database name |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis URL for Celery broker |
| `API_KEY` | *(empty)* | API key for protected endpoints |
| `JWT_SECRET` | `change-me` | Secret for JWT token signing |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiry duration |
| `SCRAPE_BASE_URL` | `https://ikman.lk` | Base URL for scraping |
| `SCRAPE_MAX_PAGES` | `5` | Max listing pages to crawl per cycle |
| `SCRAPE_DELAY` | `1.5` | Seconds between requests (polite delay) |
| `SCRAPE_USER_AGENT` | Chrome UA string | HTTP User-Agent header |
| `SCRAPE_DETAIL_PAGES` | `True` | Fetch individual ad detail pages |

---

## Repository Structure

```
AutoSenseLK/
├── docs/                          ← You are here
│   ├── project_overview.md
│   ├── api_documentation.md
│   ├── backend_structure.md
│   └── frontend_structure.md
├── vehicle-market-backend/
│   ├── app/                       ← FastAPI application
│   │   ├── api/v1/                ← REST endpoints
│   │   ├── core/                  ← Config, DB, security, logging
│   │   ├── models/                ← Beanie document models
│   │   ├── schemas/               ← Pydantic request/response schemas
│   │   ├── scraper/               ← Web scraping pipeline
│   │   ├── ml/                    ← Machine learning module
│   │   ├── analytics/             ← Market analytics logic
│   │   ├── tasks/                 ← Celery background tasks
│   │   └── main.py                ← App factory & router mount
│   ├── models_store/              ← Trained ML model files (.pkl)
│   ├── tests/                     ← Test suite
│   ├── .env / .env.example        ← Environment configuration
│   └── requirements.txt           ← Python dependencies
├── vehicle-market-frontend/
│   └── AutoSenseLK/               ← Vite + React + TypeScript app
│       ├── src/
│       │   ├── main.tsx            ← Entry point
│       │   ├── App.tsx             ← Root component
│       │   ├── LandingPage.tsx     ← Main landing page with charts
│       │   └── index.css           ← Global styles
│       ├── index.html              ← HTML template
│       └── package.json            ← Node dependencies
├── README.md
└── LICENSE
```

---

## Service Dependencies

```
┌─────────────────┐
│    Frontend      │  (Vite + React)
│  localhost:5173  │
└───────┬─────────┘
        │ HTTP API calls
        ▼
┌─────────────────┐       ┌──────────────┐
│    Backend API   │──────▶│   MongoDB    │
│  localhost:8000  │       │  :27017      │
└───────┬─────────┘       └──────────────┘
        │ (optional)
        ▼
┌─────────────────┐
│  Celery Worker   │──────▶ Redis :6379
│  (background)    │
└─────────────────┘
```

| Service | Required? | When Needed |
|---|---|---|
| **MongoDB** | ✅ Yes | Always — primary data store |
| **Redis** | ❌ Optional | Only when running Celery background tasks (scraping, ML training, snapshots) |
| **Celery Worker** | ❌ Optional | Only for scheduled/background processing |

---

## License

Private — All rights reserved.
