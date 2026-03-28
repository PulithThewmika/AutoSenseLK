import sys
with open('docs/frontend_structure.md', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('\n---\n\n# Admin Dashboard Structure')
text = parts[0]

admin_doc = '''

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
'''

with open('docs/frontend_structure.md', 'w', encoding='utf-8') as f:
    f.write(text + admin_doc)
