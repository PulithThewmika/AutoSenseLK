<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0D1117,100:161b22&height=100&section=header&text=📚%20AutoSenseLK%20Docs&fontSize=36&fontColor=58a6ff&fontAlignY=55" width="100%" />

<br/>

**Everything you need to understand, set up, and extend AutoSenseLK**

<br/>

[![Docs](https://img.shields.io/badge/Status-Up_to_Date-238636?style=for-the-badge&labelColor=0d1117)](.)
[![Pages](https://img.shields.io/badge/Pages-6_Documents-58a6ff?style=for-the-badge&labelColor=0d1117)](.)

</div>

<br/>

---

<br/>

## 📖 Documentation Index

Navigate to the guide you need — each document covers a focused area of the platform.

<br/>

<table>
<tr>
<td width="50%" valign="top">

### 🏠 Getting Started

<br/>

| Document | Description |
|:---|:---|
| 📋 [**Project Overview**](project_overview.md) | Prerequisites, quick start, environment config, and service dependencies |
| ⚙️ [**Technical Reference**](technical_reference.md) | Full architecture, database schema, scraper pipeline, ML system, and development guide |

</td>
<td width="50%" valign="top">

### 🔌 API & Backend

<br/>

| Document | Description |
|:---|:---|
| 🔌 [**API Documentation**](api_documentation.md) | All 22 REST endpoints with request/response schemas and examples |
| 🏗️ [**Backend Structure**](backend_structure.md) | Module-by-module deep dive into the FastAPI backend architecture |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🎨 Frontend & Admin

<br/>

| Document | Description |
|:---|:---|
| 🎨 [**Frontend Structure**](frontend_structure.md) | React component architecture, styling system, and UI integration points |
| ⏰ [**Scheduler**](scheduler.md) | Daily pipeline automation, retry logic, and task orchestration |

</td>
<td width="50%" valign="top">

### 🗺️ Quick Links

<br/>

- 🚀 [Quick Start Guide](project_overview.md#quick-start)
- 🔑 [Environment Variables](technical_reference.md#environment-variables)
- 📡 [API Endpoint List](api_documentation.md)
- 🗄️ [Database Schema](technical_reference.md#database-schema)
- 🕷️ [Scraper Details](technical_reference.md#scraper)
- 🤖 [ML Deal Scoring](technical_reference.md#machine-learning--deal-scoring)

</td>
</tr>
</table>

<br/>

---

<br/>

## 🏛️ Architecture at a Glance

```
   ikman.lk                    AutoSenseLK Platform
  ┌─────────┐    ┌─────────────────────────────────────────────┐
  │ 55+ brands│   │                                             │
  │ 300+ models│──▶│  🕷️ Scraper  ──▶  📊 Analytics  ──▶  🤖 ML  │
  │ 3 conditions│  │       │                │               │    │
  └─────────┘    │       ▼                ▼               ▼    │
                  │  ┌──────────────────────────────────┐       │
                  │  │          MongoDB                  │       │
                  │  └──────────────┬───────────────────┘       │
                  │                 │                            │
                  │       ┌─────────┴─────────┐                 │
                  │       ▼                   ▼                 │
                  │  🔌 REST API        🎨 React Dashboard      │
                  │  (22 endpoints)     (Charts · Deals · Brands)│
                  └─────────────────────────────────────────────┘
```

<br/>

---

<br/>

<div align="center">

**Part of the [AutoSenseLK](../README.md) platform** · Sri Lanka's Vehicle Market Intelligence

</div>
