<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:1a1b27,100:009688&height=180&section=header&text=AutoSenseLK%20Backend&fontSize=48&fontColor=e6ecf4&fontAlignY=35&desc=The%20Engine%20Behind%20Sri%20Lanka's%20Vehicle%20Market%20Intelligence&descSize=16&descAlignY=55&descColor=8b949e&animation=fadeIn" width="100%" />

<br/>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=3000&pause=1000&color=009688&center=true&vCenter=true&repeat=true&width=600&height=50&lines=22+REST+API+endpoints;Daily+analytics+across+55%2B+brands;ML-powered+deal+scoring+engine;Automated+scraping+pipeline" alt="Typing Animation" />
</p>

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI_0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB_6+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Celery](https://img.shields.io/badge/Celery_5-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)

</div>

<br/>

---

<br/>

## ⚡ What This Powers

The backend is the brain of AutoSenseLK — it scrapes, cleans, analyzes, scores, and serves Sri Lanka's most comprehensive vehicle market data through a high-performance async API.

<br/>

<table>
<tr>
<td width="50%" valign="top">

### 🕷️ Scraper Pipeline
Crawls **ikman.lk** daily across 55+ brands and 300+ models. Automatically parses listings, normalises prices, and deduplicates data with SHA-256 hashing.

### 📊 Analytics Engine
Computes daily market snapshots at **4 levels of granularity** — market-wide, per-brand, per-brand×condition, and per-model×year×condition.

### 🤖 ML Deal Scoring
Compares every listing against rolling market averages and classifies deals as **good deal**, **fair**, or **overpriced** — giving buyers instant confidence.

</td>
<td width="50%" valign="top">

### 🔌 22 REST Endpoints
From paginated listings to depreciation curves, full-text search to scrape triggers — the API covers every angle of market intelligence.

### 🔄 Background Tasks
Celery + Redis power scheduled scraping, analytics computation, and ML model retraining — all running autonomously.

### 🛡️ Security
JWT authentication, API key validation, and bcrypt password hashing keep the platform secure.

</td>
</tr>
</table>

<br/>

---

<br/>

## 🚀 Quick Start

```bash
# 1. Set up environment
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# 2. Configure
cp .env.example .env    # Edit with your MongoDB URL

# 3. Launch
uvicorn app.main:app --reload
```

> 🟢 **API**: http://localhost:8000 &nbsp;·&nbsp; 📖 **Swagger**: http://localhost:8000/docs &nbsp;·&nbsp; 📘 **ReDoc**: http://localhost:8000/redoc

<br/>

---

<br/>

## 🏗️ Module Overview

```
app/
├── api/v1/           → 22 REST endpoints (listings, analytics, deals, search, scrape)
├── scraper/          → Spider, parser, cleaner, deduplicator, storage pipeline
├── analytics/        → 4-level daily snapshot engine, trends, depreciation curves
├── ml/               → Deal scorer, price predictor, model trainer
├── models/           → Beanie MongoDB document schemas
├── schemas/          → Pydantic request/response types
├── core/             → Config, database, security, logging
├── tasks/            → Celery workers + APScheduler daily pipeline
└── main.py           → App factory, router mount, startup seeder
```

<br/>

---

<br/>

## 🔌 API Highlights

| | Endpoint | What It Does |
|:---:|---|---|
| 📋 | `GET /api/v1/listings/` | Paginated listings with make, model, price, year filters |
| 📊 | `GET /api/v1/analytics/daily` | Today's market snapshot — prices, counts, trends |
| 💰 | `GET /api/v1/deals/score` | AI deal quality score for any listing |
| 📈 | `GET /api/v1/analytics/trends` | Monthly price trend data |
| 📉 | `GET /api/v1/analytics/depreciation` | Year-by-year depreciation curves |
| 🔍 | `GET /api/v1/search/` | Full-text search across all listings |
| 🕷️ | `POST /api/v1/scrape/trigger` | Trigger a full market scrape cycle |
| 🏷️ | `GET /api/v1/makes/` | All brands with model counts |

> 📖 **Full API docs**: [docs/api_documentation.md](../docs/api_documentation.md)

<br/>

---

<br/>

## 🐳 Docker

```bash
docker compose up --build
```

Starts FastAPI + MongoDB + Redis + Celery worker — everything in one command.

<br/>

---

<br/>

## 📖 Documentation

| Document | Description |
|:---|:---|
| ⚙️ [**Technical Reference**](../docs/technical_reference.md) | Architecture, database schema, scraper pipeline, ML system |
| 🔌 [**API Documentation**](../docs/api_documentation.md) | All 22 endpoints with request/response schemas |
| 🏗️ [**Backend Structure**](../docs/backend_structure.md) | Module-by-module deep dive |
| ⏰ [**Scheduler**](../docs/scheduler.md) | Daily pipeline, retry logic, task orchestration |

<br/>

---

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:1a1b27,100:009688&height=100&section=footer" width="100%" />

**Part of the [AutoSenseLK](../README.md) platform** · Sri Lanka's Vehicle Market Intelligence

</div>
