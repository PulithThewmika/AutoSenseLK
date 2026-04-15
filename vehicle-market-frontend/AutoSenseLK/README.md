<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0b0f15,50:111820,100:00c29a&height=180&section=header&text=AutoSenseLK%20Frontend&fontSize=48&fontColor=e6ecf4&fontAlignY=35&desc=The%20Face%20of%20Sri%20Lanka's%20Vehicle%20Market%20Intelligence&descSize=16&descAlignY=55&descColor=8b949e&animation=fadeIn" width="100%" />

<br/>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=3000&pause=1000&color=00C29A&center=true&vCenter=true&repeat=true&width=600&height=50&lines=Interactive+market+dashboard;Real-time+price+trend+charts;AI+deal+scoring+interface;Beautiful+dark-theme+UI" alt="Typing Animation" />
</p>

<br/>

![React](https://img.shields.io/badge/React_19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite_8-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

</div>

<br/>

---

<br/>

## 🎨 What This Is

The public-facing dashboard where users explore Sri Lanka's vehicle market — browse live pricing data, discover good deals, track depreciation trends, and compare brands. Built with a stunning dark-theme glassmorphism design that makes data beautiful.

<br/>

---

<br/>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🏠 Market Dashboard
Live market overview with stat cards showing total listings, average prices, best deals, and market health — all at a glance.

### 📈 Interactive Price Charts
Chart.js-powered visualizations tracking price trends across Toyota, Honda, Suzuki, Nissan, and more. Toggle between 6M, 1Y, and All-time views.

### 💰 Deal Scoring UI
Paste any listing and get an instant AI verdict — **good deal**, **fair**, or **overpriced** — with savings calculation and market comparison.

</td>
<td width="50%" valign="top">

### 🏷️ Brand Explorer
Dive into any of 55+ brands to see model breakdowns, condition comparisons (new vs used vs reconditioned), and pricing heat maps.

### 📊 Analytics Tab
Deep market analytics — depreciation curves, mileage impact charts, monthly trend lines, and daily snapshot comparisons.

### 🎨 Premium Design
Dark-theme glassmorphism with animated gradient orbs, infinite price tickers, reveal-on-scroll animations, and custom typography (Syne + DM Sans + DM Mono).

</td>
</tr>
</table>

<br/>

---

<br/>

## 🖥️ UI Sections

<div align="center">

```
┌──────────────────────────────────────────┐
│  🧭 Navigation Bar                       │
│  Logo · Market · Compare · Trends · CTA  │
├──────────────────────────────────────────┤
│  🌟 Hero Section                         │
│  Animated orbs · Tagline · Stat cards    │
├──────────────────────────────────────────┤
│  📈 Live Price Trend Chart               │
│  4 models · Time range selector          │
├──────────────────────────────────────────┤
│  💹 Price Ticker                         │
│  Infinite scrolling marquee              │
├──────────────────────────────────────────┤
│  📊 Stats Strip · Feature Grid           │
│  6 key metrics · 6 feature cards         │
├──────────────────────────────────────────┤
│  💰 Deal Intelligence Preview            │
│  AI scoring demo · Savings calculation   │
├──────────────────────────────────────────┤
│  ⚙️ How It Works                         │
│  Scrape → Clean → Analyse → Decide      │
├──────────────────────────────────────────┤
│  🚀 CTA · Footer                        │
└──────────────────────────────────────────┘
```

</div>

<br/>

---

<br/>

## 🎭 Design System

<div align="center">

| | Element | Details |
|:---:|---|---|
| 🌑 | **Theme** | Dark-first with glassmorphism cards (`backdrop-filter: blur`) |
| 🎨 | **Accent** | `#00c29a` — vibrant green for CTAs and highlights |
| ✍️ | **Headings** | Syne (600–800 weight) — bold, modern display font |
| 📝 | **Body** | DM Sans (300–500) — clean, readable |
| 🔢 | **Data** | DM Mono (300–400) — perfect for prices and chart labels |
| ✨ | **Animations** | Gradient orbs, reveal-on-scroll, infinite ticker, smooth transitions |

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

> 🟢 **App**: http://localhost:5173

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
├── App.tsx                → Root: theme management, tab routing
├── components/
│   ├── Navigation.tsx     → Top navbar with logo, links, theme toggle
│   ├── TabBar.tsx         → Tab switcher (Home · Analytics · Brands · Deals)
│   ├── Footer.tsx         → Site footer with links
│   └── tabs/
│       ├── HomeTab.tsx    → Market dashboard with stat cards & charts
│       ├── AnalyticsTab.tsx → Price trends, depreciation, mileage curves
│       ├── BrandsTab.tsx  → Brand explorer with model breakdowns
│       └── DealsTab.tsx   → Deal scoring interface
├── services/
│   └── api.ts             → Backend API client (all endpoint bindings)
├── data/                  → Static/mock data
├── index.css              → Complete design system (~24KB)
└── main.tsx               → Entry point
```

<br/>

---

<br/>

## 📖 Documentation

| Document | Description |
|:---|:---|
| 🎨 [**Frontend Structure**](../../docs/frontend_structure.md) | Full component architecture and styling deep dive |
| ⚙️ [**Technical Reference**](../../docs/technical_reference.md) | Platform architecture and API overview |
| 🔌 [**API Documentation**](../../docs/api_documentation.md) | All backend endpoints this frontend consumes |

<br/>

---

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0b0f15,50:111820,100:00c29a&height=100&section=footer" width="100%" />

**Part of the [AutoSenseLK](../../README.md) platform** · Sri Lanka's Vehicle Market Intelligence

</div>
