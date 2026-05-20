<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:1a1b27,100:238636&height=220&section=header&text=AutoSenseLK&fontSize=72&fontColor=58a6ff&fontAlignY=35&desc=Sri%20Lanka's%20Vehicle%20Market%20Intelligence%20Platform&descSize=18&descAlignY=55&descColor=8b949e&animation=fadeIn" width="100%" />

<br/>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=80&lines=Real-time+market+data+from+55%2B+brands;AI-powered+deal+scoring+%26+price+predictions;Daily+analytics+across+300%2B+vehicle+models" alt="Typing Animation" />
</p>

<br/>

<!-- Badges Row 1 — Status -->
[![Live Data](https://img.shields.io/badge/📊_Live_Data-55+_Brands-238636?style=for-the-badge&labelColor=0d1117)](docs/technical_reference.md)
[![Models Tracked](https://img.shields.io/badge/🚗_Models-300+-58a6ff?style=for-the-badge&labelColor=0d1117)](docs/technical_reference.md)
[![API Endpoints](https://img.shields.io/badge/🔌_API-22_Endpoints-f78166?style=for-the-badge&labelColor=0d1117)](docs/api_documentation.md)
[![ML Powered](https://img.shields.io/badge/🤖_ML-Deal_Scoring-a371f7?style=for-the-badge&labelColor=0d1117)](docs/technical_reference.md#machine-learning--deal-scoring)

<br/>

<!-- Badges Row 2 — Tech -->
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_19-61DAFB?style=flat-square&logo=react&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)

</div>

<br/>

---

<br/>

## 🎯 The Problem

> Buying or selling a vehicle in Sri Lanka? **You're flying blind.**
>
> Prices vary wildly across listings. There's no reliable benchmark for what a car is *actually* worth. Sellers overprice. Buyers overpay. Nobody knows if they're getting a fair deal.

<br/>

## 💡 The Solution

**AutoSenseLK** is a market intelligence platform that collects, analyzes, and visualizes real-time vehicle pricing data across Sri Lanka — so you can make decisions backed by data, not guesswork.

<div align="center">

```
📡 COLLECT          📊 ANALYZE          🎯 DECIDE
   │                   │                   │
   ▼                   ▼                   ▼
Scrape 55+       Daily snapshots      Know if a deal
brands daily     across 4 levels      is good, fair,
from ikman.lk    of granularity       or overpriced
```

</div>

<br/>

---

<br/>

## ✨ What AutoSenseLK Does

<table>
<tr>
<td width="50%" valign="top">

### 📊 Market Dashboard
A beautiful, real-time dashboard showing market health at a glance — total listings, average prices, top brands, and daily trends. Powered by interactive Chart.js visualizations.

### 🔍 Smart Search
Search across thousands of listings by make, model, year, price range, condition, or location. Find exactly what you're looking for in seconds.

### 💰 Deal Scoring
Our AI compares every listing against market averages and instantly labels it as a **good deal**, **fair**, or **overpriced** — so you never overpay again.

</td>
<td width="50%" valign="top">

### 📈 Price Trends
Track how prices move month by month. See depreciation curves by year. Understand how mileage affects value. Make timing-based buying decisions.

### 🏷️ Brand Intelligence
Deep analytics for every major brand — Toyota, Honda, Suzuki, BMW, Mercedes-Benz, and 50+ more. See which brands hold value and which depreciate fastest.

### 🔄 Daily Updates
The platform automatically refreshes its data daily, computing fresh analytics across all brands, models, and conditions at midnight — no manual work needed.

</td>
</tr>
</table>

<br/>

---

<br/>

## 🚀 Key Highlights

<div align="center">

| | Feature | Details |
|:---:|---|---|
| 🕷️ | **Comprehensive Coverage** | 55+ brands, 300+ models, 3 conditions (new, used, reconditioned) |
| 📊 | **4-Level Analytics** | Market-wide → Brand → Brand×Condition → Model×Year×Condition |
| 🤖 | **ML Deal Scoring** | Instant good/fair/overpriced classification per listing |
| 📈 | **Depreciation Curves** | Year-by-year and mileage-based price decline tracking |
| 🔌 | **22 REST Endpoints** | Full API with Swagger UI for developers & integrations |
| 🗄️ | **Smart Deduplication** | SHA-256 hashing prevents data pollution |
| ⚡ | **Async Architecture** | Non-blocking scraping + async database operations |
| 🐳 | **Docker Ready** | One command to run the entire stack |

</div>

<br/>

---

<br/>

## 🏗️ How It Works

<div align="center">

```
                    ┌─────────────────────────┐
                    │      🌐 ikman.lk         │
                    │   Sri Lanka's #1 Market   │
                    └────────────┬──────────────┘
                                 │
                         ┌───────▼───────┐
                         │  🕷️ Scraper   │
                         │   Pipeline     │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                   │
        ┌─────▼─────┐    ┌──────▼──────┐    ┌──────▼──────┐
        │  🧹 Clean  │    │ 🔐 Dedup   │    │ 💾 Store    │
        │ & Parse    │    │ (SHA-256)   │    │ (MongoDB)   │
        └─────┬─────┘    └──────┬──────┘    └──────┬──────┘
              │                  │                   │
              └──────────────────┼──────────────────┘
                                 │
                         ┌───────▼───────┐
                         │ 📊 Analytics  │
                         │   Engine      │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                   │
        ┌─────▼─────┐    ┌──────▼──────┐    ┌──────▼──────┐
        │  🔌 REST │     │ 🤖 ML Deal │    │ 📈 React   │
        │   API     │    │  Scoring    │    │ Dashboard   │
        └───────────┘    └─────────────┘    └─────────────┘
```

</div>

<br/>

---

<br/>

## 🏎️ Brands We Track

<div align="center">

| Premium | Japanese | Korean & Others |
|:---:|:---:|:---:|
| 🇩🇪 Mercedes-Benz (47 models) | 🇯🇵 Toyota (68 models) | 🇰🇷 Kia (17 models) |
| 🇩🇪 BMW (50 models) | 🇯🇵 Honda (26 models) | 🇯🇵 Daihatsu (17 models) |
| 🇩🇪 Audi (13 models) | 🇯🇵 Suzuki (28 models) | 🇯🇵 Mitsubishi (23 models) |
| 🇬🇧 Land Rover (9 models) | 🇯🇵 Nissan (35 models) | **+ 44 more brands** |

</div>

> **Total**: 55+ brands × 300+ models × 3 conditions = the most comprehensive vehicle market dataset in Sri Lanka.

<br/>

---

<br/>

## 🖥️ Screenshots

<div align="center">

> 🚧 **Coming Soon** — Screenshots of the live dashboard, deal scoring UI, and analytics charts will be added here.

</div>

<br/>

---

<br/>

## 🛠️ Getting Started

Get the full platform running in under 5 minutes.

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/PulithThewmika/AutoSenseLK.git
cd AutoSenseLK

# 2. Start the backend
cd vehicle-market-backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# 3. Start the frontend (new terminal)
cd vehicle-market-frontend/AutoSenseLK
npm install && npm run dev
```

### Or use Docker

```bash
cd vehicle-market-backend
docker compose up --build
```

> 📖 **Full setup guide**: [docs/project_overview.md](docs/project_overview.md) — includes environment variables, prerequisites, and service dependencies.

<br/>

---

<br/>

## 📖 Documentation

<div align="center">

| Document | What's Inside |
|:---|:---|
| 📋 [**Project Overview**](docs/project_overview.md) | Full setup guide, prerequisites, environment config |
| 🔌 [**API Documentation**](docs/api_documentation.md) | All 22 endpoints with request/response examples |
| ⚙️ [**Technical Reference**](docs/technical_reference.md) | Architecture, database schema, scraper pipeline, ML system |
| 🏗️ [**Backend Structure**](docs/backend_structure.md) | Module-by-module backend deep dive |
| 🎨 [**Frontend Structure**](docs/frontend_structure.md) | React components, API integration, UI architecture |
| ⏰ [**Scheduler**](docs/scheduler.md) | Daily pipeline, retry logic, task orchestration |

</div>

<br/>

---

<br/>

## 🗺️ Roadmap

- [x] Multi-brand scraping with model-level granularity
- [x] 4-level daily analytics engine
- [x] ML-powered deal scoring
- [x] Interactive React dashboard with Chart.js
- [x] Full REST API with 22 endpoints
- [x] Docker deployment
- [ ] Price alert notifications
- [ ] Mobile-responsive PWA
- [ ] Historical price comparison tool
- [ ] WhatsApp/Telegram bot integration
- [ ] Dealer reputation scoring

<br/>

---

<br/>

<div align="center">

## 🤝 Contributing

AutoSenseLK is currently a private project. If you're interested in contributing or have feedback, feel free to open an issue.

<br/>

## 📄 License

All rights reserved.

<br/>

---
<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:1a1b27,100:238636&height=120&section=footer" width="100%" />

<br/>

**Built with ❤️ for Sri Lanka's vehicle market**

<sub>Automating market intelligence so you never overpay for a vehicle again.</sub>

</div>
