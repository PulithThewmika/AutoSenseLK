<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161b22,100:a371f7&height=180&section=header&text=AutoSenseLK%20Admin&fontSize=48&fontColor=e6ecf4&fontAlignY=35&desc=Operations%20Dashboard%20for%20Platform%20Management&descSize=16&descAlignY=55&descColor=8b949e&animation=fadeIn" width="100%" />

<br/>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=3000&pause=1000&color=A371F7&center=true&vCenter=true&repeat=true&width=600&height=50&lines=Real-time+service+monitoring;One-click+scraper+controls;Live+server+log+streaming;Database+%26+system+health+views" alt="Typing Animation" />
</p>

<br/>

![React](https://img.shields.io/badge/React_19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite_8-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socket.io&logoColor=white)

</div>

<br/>

---

<br/>

## 🎛️ What This Is

The internal operations dashboard for AutoSenseLK administrators. Monitor platform health, control the scraping pipeline, stream live server logs, track database metrics, and manage the entire system — all from a sleek, real-time interface.

<br/>

---

<br/>

## ✨ Dashboard Panels

<table>
<tr>
<td width="50%" valign="top">

### 📊 Overview
Live KPI cards with sparkline charts — total listings, API requests/min, average response time, and error rate. Includes service status table showing health of FastAPI, MongoDB, Celery, Redis, and Playwright.

### 🕷️ Scraper Controls
Trigger full market scrapes or targeted brand-specific crawls with one click. Brand selector dropdown with all 55+ supported brands. Live scrape status and pipeline stage tracking.

### 📈 Analytics
Deep analytics dashboards powered by Chart.js — market trends, brand comparisons, and data volume metrics.

</td>
<td width="50%" valign="top">

### 📋 Live Logs
Real-time server log streaming via **WebSocket** connection. Color-coded log levels, auto-scroll, and up to 100 entries in the live buffer. Connect to `ws://localhost:8000/api/v1/logs/stream`.

### 🗄️ Database
MongoDB collection health, document counts, index status, and storage metrics at a glance.

### ⚙️ System
System resource monitoring — CPU, memory, disk usage, and uptime tracking for all platform services.

### 🔔 Alerts
Configurable threshold alerts for error rates, response times, scrape failures, and data anomalies.

</td>
</tr>
</table>

<br/>

---

<br/>

## 🖥️ Dashboard Layout

<div align="center">

```
┌──────────┬───────────────────────────────────┐
│          │  📌 Topbar (title · theme toggle)  │
│  📁      ├───────────────────────────────────┤
│  Sidebar │                                    │
│          │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │
│  Overview│  │ KPI │ │ KPI │ │ KPI │ │ KPI │ │
│  Analytics│ └─────┘ └─────┘ └─────┘ └─────┘ │
│  Logs    │                                    │
│  Database│  ┌──────────────┐ ┌──────────────┐│
│  System  │  │  Req/min     │ │  Response    ││
│  Alerts  │  │  Chart 📈    │ │  Time 📉     ││
│          │  └──────────────┘ └──────────────┘│
│          │                                    │
│          │  ┌────────┐ ┌────────┐ ┌────────┐ │
│          │  │Service │ │Scraper │ │Pipeline│ │
│          │  │ Status │ │Controls│ │ Status │ │
│          │  └────────┘ └────────┘ └────────┘ │
└──────────┴───────────────────────────────────┘
```

</div>

<br/>

---

<br/>

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

> 🟣 **Dashboard**: http://localhost:5174

<br/>

### Available Scripts

| Script | Description |
|:---|:---|
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Type-check + production build |
| `npm run lint` | Run ESLint checks |
| `npm run preview` | Preview production build locally |

<br/>

---

<br/>

## 🧩 Component Architecture

```
src/
├── App.tsx                → Root: sidebar routing, theme management
├── components/
│   ├── Sidebar.tsx        → Navigation sidebar (6 sections)
│   └── Topbar.tsx         → Header bar with title & theme toggle
├── pages/
│   ├── Overview.tsx       → KPIs, sparklines, service status, scraper controls
│   ├── Analytics.tsx      → Market analytics charts & data visualizations
│   ├── Logs.tsx           → Live WebSocket log streaming
│   ├── Database.tsx       → MongoDB health & collection metrics
│   ├── System.tsx         → System resource monitoring
│   └── Alerts.tsx         → Threshold alerts configuration
├── services/
│   └── api.ts             → Backend API client bindings
├── utils/
│   └── ChartHelpers.ts   → Chart.js config factories (sparklines, line charts)
├── index.css              → Admin dashboard design system
└── main.tsx               → Entry point
```

<br/>

---

<br/>

## 🔗 Backend Integration

The admin dashboard connects to the AutoSenseLK backend API:

| Feature | Endpoint | Method |
|:---|:---|:---:|
| Market Stats | `/api/v1/analytics/summary` | `GET` |
| Health Check | `/health` | `GET` |
| Scrape Status | `/api/v1/scrape/status` | `GET` |
| Trigger Full Scrape | `/api/v1/scrape/trigger` | `POST` |
| Trigger Brand Scrape | `/api/v1/scrape/trigger/brand/{brand}` | `POST` |
| Available Brands | `/api/v1/scrape/brands` | `GET` |
| Live Logs | `ws://localhost:8000/api/v1/logs/stream` | `WS` |

<br/>

---

<br/>

## 📖 Documentation

| Document | Description |
|:---|:---|
| 🎨 [**Frontend Structure**](../docs/frontend_structure.md) | Includes admin dashboard component docs |
| ⚙️ [**Technical Reference**](../docs/technical_reference.md) | Platform architecture and API overview |
| 🔌 [**API Documentation**](../docs/api_documentation.md) | All backend endpoints this dashboard uses |

<br/>

---

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161b22,100:a371f7&height=100&section=footer" width="100%" />

**Part of the [AutoSenseLK](../README.md) platform** · Sri Lanka's Vehicle Market Intelligence

</div>
