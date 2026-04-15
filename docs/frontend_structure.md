# Frontend Structure

> **Location**: `vehicle-market-frontend/AutoSenseLK/`  
> **Framework**: React 19 + TypeScript  
> **Build Tool**: Vite 8  
> **Entry Point**: `npm run dev`  
> **URL**: http://localhost:5173

---

## Directory Layout

```
vehicle-market-frontend/
└── AutoSenseLK/
    ├── public/                  ← Static assets (favicon, etc.)
    ├── src/
    │   ├── main.tsx             ← App entry point (renders root)
    │   ├── App.tsx              ← Root component (renders LandingPage)
    │   ├── LandingPage.tsx      ← Full landing page with all sections
    │   ├── index.css            ← Global stylesheet (all styles)
    │   └── assets/              ← Images and other assets
    ├── index.html               ← HTML template with fonts & meta tags
    ├── package.json             ← Dependencies & scripts
    ├── vite.config.ts           ← Vite configuration
    ├── tsconfig.json            ← TypeScript base config
    ├── tsconfig.app.json        ← App-specific TS config
    ├── tsconfig.node.json       ← Node-specific TS config
    └── eslint.config.js         ← ESLint configuration
```

---

## Dependencies

### Runtime

| Package | Version | Purpose |
|---|---|---|
| `react` | ^19.2.4 | UI library |
| `react-dom` | ^19.2.4 | DOM rendering |
| `chart.js` | ^4.5.1 | Charting library |
| `react-chartjs-2` | ^5.3.1 | React wrapper for Chart.js |

### Dev Dependencies

| Package | Version | Purpose |
|---|---|---|
| `vite` | ^8.0.0 | Build tool & dev server |
| `@vitejs/plugin-react` | ^6.0.0 | React support for Vite |
| `typescript` | ~5.9.3 | Type checking |
| `eslint` | ^9.39.4 | Code linting |
| `eslint-plugin-react-hooks` | ^7.0.1 | React hooks lint rules |
| `eslint-plugin-react-refresh` | ^0.5.2 | Fast refresh lint rules |

---

## NPM Scripts

| Script | Command | Description |
|---|---|---|
| `dev` | `vite` | Start dev server with HMR |
| `build` | `tsc -b && vite build` | Type-check & production build |
| `lint` | `eslint .` | Run ESLint on all files |
| `preview` | `vite preview` | Preview production build locally |

---

## Component Architecture

### `main.tsx` — Entry Point

- Renders `<App />` inside `<StrictMode>`
- Imports global `index.css` stylesheet
- Mounts to `#root` DOM element

### `App.tsx` — Root Component

- Minimal wrapper that renders `<LandingPage />`
- Will expand to include routing when more pages are added

### `LandingPage.tsx` — Main Page

The landing page is a single-component design with the following sections:

#### 1. Navigation Bar
- Logo: **AutoSenseLK**
- Nav links: Market, Compare, Trends, Alerts, About
- CTA buttons: Sign in (ghost), Get started (primary)

#### 2. Hero Section
- Animated background orbs (CSS animations)
- Tagline: *"Sense the true price of any car"*
- Description of the platform's ML-powered capabilities
- CTA buttons: "Explore market", "Check a listing"
- Stat cards:
  - Average Market Price (Rs. 8.4M)
  - Listings Tracked (24,810)
  - Best Deal Today

#### 3. Interactive Price Trend Chart
- Built with Chart.js (`<Line>` component)
- Tracks 4 models: Toyota Aqua, Honda Vezel, Suzuki Alto, Nissan Leaf
- Time range selector: **6M** / **1Y** / **All**
- Gradient fills under chart lines
- Custom tooltips with formatted prices
- Data is currently hardcoded (to be connected to backend API)

#### 4. Live Price Ticker
- Horizontally scrolling marquee of vehicle prices
- Shows make, price, and percentage change (↑/↓)
- Infinite scroll animation via CSS

#### 5. Stats Strip
- Key metrics in a horizontal bar:
  - 4,210+ new listings/week
  - 38 makes tracked
  - Rs. 4.1M median price
  - 12.4% listings = good deals
  - 25 districts covered
  - 6h scrape frequency

#### 6. Features Grid
- 6 feature cards in a responsive grid:
  1. 📊 Live price tracking
  2. 🤖 ML deal scoring
  3. 📈 Price trend charts
  4. 🔔 Price alerts
  5. 🗺️ Location insights
  6. ⚖️ Model comparison

#### 7. Deal Intelligence Preview
- Mock deal scoring card showing:
  - Vehicle: Toyota Aqua S (2016, 68k km, Hybrid, Colombo)
  - Label: "Good deal"
  - Listed vs market average price
  - Animated price bar visualisation
  - Savings calculation (Rs. 670,000 / 9.0% below avg)

#### 8. How It Works
- 4-step pipeline explanation:
  1. We scrape (ikman.lk every 6h)
  2. We clean (normalise, deduplicate)
  3. We analyse (ML fair pricing)
  4. You decide (dashboards & scores)

#### 9. CTA Section
- "Stop guessing. Start sensing."
- Buttons: "Explore the market free", "View live dashboard"

#### 10. Footer
- Logo, nav links, copyright notice

---

## Styling

### `index.css` — Global Stylesheet

All styles are in a single CSS file (~15KB). Key design decisions:

#### Design System

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#0b0f15` | Page background (dark) |
| `--surface` | `#111820` | Card backgrounds |
| `--border` | `rgba(255,255,255,0.06)` | Subtle borders |
| `--text` | `#e6ecf4` | Primary text (light) |
| `--muted` | `#4a5d74` | Secondary text |
| `--accent` | `#00c29a` | Green accent (CTAs, highlights) |

#### Typography

| Font | Usage |
|---|---|
| **Syne** (600–800) | Headings, hero text |
| **DM Sans** (300–500) | Body text, descriptions |
| **DM Mono** (300–400) | Chart labels, data values |

#### Key CSS Features
- **Dark theme** with glassmorphism effects (`backdrop-filter: blur`)
- **Animated gradient orbs** in hero section (CSS `@keyframes`)
- **Reveal-on-scroll** animations via IntersectionObserver + CSS transitions
- **Infinite ticker** animation for price marquee
- **Responsive design** with media queries for mobile
- **Smooth chart tooltips** with custom styling

---

## Fonts & SEO

### `index.html`

- **Title**: "AutoSenseLK — Sri Lanka Vehicle Market Intelligence"
- **Meta description**: Describes the ML-powered vehicle price tracking platform
- **Google Fonts**: Preconnected and loaded (Syne, DM Sans, DM Mono)
- **Favicon**: SVG format (`/favicon.svg`)

---

## Current State & Future Needs

### ✅ Implemented
- Landing page with all sections and animations
- Interactive Chart.js price trend visualisation
- Responsive dark-theme design
- Static/mock data throughout

### 🔧 Needs Implementation

| Feature | Description |
|---|---|
| **React Router** | Add routing for multi-page navigation (Market, Compare, Trends, etc.) |
| **API Integration** | Connect to backend API for real-time data (listings, analytics, trends) |
| **Search Page** | Interface for searching and filtering vehicle listings |
| **Market Dashboard** | Live dashboard with real data from `/api/v1/analytics/daily` |
| **Deal Checker** | Form to paste ikman.lk URL and get deal score from `/api/v1/deals/score` |
| **Comparison Page** | Side-by-side model comparison using analytics data |
| **Trend Visualisations** | Connect chart to `/api/v1/analytics/trends` for real data |
| **Authentication** | Sign in / Sign up flow using JWT tokens |
| **Price Alerts** | User-configurable alerts for target prices |
| **State Management** | Consider Zustand or React Context for global state |
| **Error Handling** | Loading states, error boundaries, empty states |
| **Component Splitting** | Break `LandingPage.tsx` into reusable components |






---

# Admin Dashboard Structure

> **Location**: `vehicle-market-admindash/`
> **Framework**: React 19 + TypeScript
> **Build Tool**: Vite 8
> **Entry Point**: `npm run dev`
> **URL**: http://localhost:5174

---

## Directory Layout

```text
vehicle-market-admindash/
├── public/                  ← Static assets
├── src/
│   ├── main.tsx             ← App entry point
│   ├── App.tsx              ← Root component with React Router
│   ├── index.css            ← Global admin Tailwind/CSS styles
│   ├── components/          ← Reusable UI components
│   │   ├── Sidebar.tsx      ← Main navigation sidebar
│   │   └── ...
│   └── pages/
│       ├── Overview.tsx     ← Market stats (live API data) & Scraper control tile
│       ├── Logs.tsx         ← Live backend server logs via WebSocket streamer
│       └── ...
├── index.html               ← HTML template
├── package.json             ← Dependencies & scripts
├── vite.config.ts           ← Vite configuration
└── tsconfig.json            ← TypeScript config
```

## Features & Integration

### ✅ Implemented
- **React Router Navigation**: Multi-page routing via `react-router-dom` (Overview, Logs, Makes, etc.).
- **Live Scraper Control (Overview.tsx)**: Replaced mock data with live bindings. Users can trigger full database scrapes by sending API requests to `POST /api/v1/scrape/trigger` and track status via `GET /api/v1/scrape/status`.
- **Live Logs Streaming (Logs.tsx)**: Utilizes native browser `WebSocket` APIs to connect with backend route `ws://localhost:8000/api/v1/logs/stream`. Dynamically queues logs up to 100 entries showing level gradients.

### 🔧 Needs Implementation
- Implement Authentication & API key enforcement since endpoints like `/scrape/trigger` are currently unprotected.
- Connect additional mock-data dashboard pieces (like Deal Statistics, Latest Listings) to actual backend datasets.
