# API Documentation

> **Base URL**: `http://localhost:8000`  
> **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI) | `http://localhost:8000/redoc` (ReDoc)  
> **API Prefix**: `/api/v1`

---

## Table of Contents

- [Health Check](#health-check)
- [Listings](#listings)
- [Analytics](#analytics)
- [Deal Scoring](#deal-scoring)
- [Makes & Models](#makes--models)
- [Search](#search)
- [Scraper](#scraper)
  - [Logs](#logs)
---

## Health Check

### `GET /health`

Basic health check to verify the API is running.

**Response:**

```json
{
  "status": "ok"
}
```

---

## Listings

### `GET /api/v1/listings/`

Return paginated vehicle listings with optional filters.

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | `int` | `1` | Page number (≥ 1) |
| `size` | `int` | `20` | Items per page (1–100) |
| `make` | `string` | `null` | Filter by vehicle make (e.g. "Toyota") |
| `model` | `string` | `null` | Filter by vehicle model (e.g. "Aqua") |
| `min_price` | `float` | `null` | Minimum price (LKR) |
| `max_price` | `float` | `null` | Maximum price (LKR) |
| `year_from` | `int` | `null` | Minimum manufacturing year |
| `year_to` | `int` | `null` | Maximum manufacturing year |

**Example Request:**

```
GET /api/v1/listings/?page=1&size=10&make=Toyota&model=Aqua&min_price=5000000
```

**Response:**

```json
{
  "page": 1,
  "size": 10,
  "total": 142,
  "results": [
    {
      "id": "6650af...",
      "title": "Toyota Aqua S 2016",
      "price": 7680000.0,
      "currency": "LKR",
      "mileage": 68000.0,
      "year": 2016,
      "location": "Colombo",
      "source_url": "https://ikman.lk/en/ad/...",
      "make": "Toyota",
      "model": "Aqua",
      "condition": "used",
      "category": "Cars",
      "posted_date": "2026-03-15",
      "created_at": "2026-03-15T12:00:00Z"
    }
  ]
}
```

---

### `GET /api/v1/listings/{listing_id}`

Return a single listing by its MongoDB ObjectId.

| Parameter | Type | Description |
|---|---|---|
| `listing_id` | `string` | MongoDB ObjectId |

---

## Analytics

### `GET /api/v1/analytics/avg-price`

Return the average price across listings, optionally filtered by make and/or model.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | `string` | `null` | Filter by make name |
| `model` | `string` | `null` | Filter by model name |

**Response:**

```json
{
  "make": "Toyota",
  "model": "Aqua",
  "avg_price": 7420000.0,
  "sample_count": 34
}
```

---

### `GET /api/v1/analytics/trends`

Return monthly price trends for a make/model over a specified number of months.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | `string` | `null` | Filter by make name |
| `model` | `string` | `null` | Filter by model name |
| `months` | `int` | `12` | Number of months of history (1–60) |

---

### `GET /api/v1/analytics/summary`

Return overall market statistics: total listings, average price, unique makes/models count.

---

### `GET /api/v1/analytics/depreciation`

Return price-vs-year depreciation curve (avg price per manufacturing year).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | `string` | `null` | Filter by make |
| `model` | `string` | `null` | Filter by model |

---

### `GET /api/v1/analytics/mileage`

Return price-vs-mileage curve bucketed by 25,000 km bands.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | `string` | `null` | Filter by make |
| `model` | `string` | `null` | Filter by model |

---

### `GET /api/v1/analytics/daily`

Return the latest market-wide daily analytics snapshot.

---

### `GET /api/v1/analytics/daily/brands`

Return the latest daily snapshot for every brand, sorted by listing count.

---

### `GET /api/v1/analytics/daily/brand/{brand}`

Return the latest daily snapshot for a specific brand, with condition breakdown (used, brand_new, reconditioned).

---

### `GET /api/v1/analytics/daily/brand/{brand}/{condition}`

Return the latest snapshot for a specific brand + condition combination.

---

### `GET /api/v1/analytics/daily/history`

Return historical daily analytics snapshots.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `days` | `int` | `30` | Number of days (1–365) |
| `scope` | `string` | `"market"` | `"market"`, `"brand"`, or `"brand_condition"` |
| `brand` | `string` | `null` | Filter by brand (optional) |

---

## Deal Scoring

### `GET /api/v1/deals/score`

Return the deal score for a specific listing. Compares the listing's actual price against the average price of similar listings (same make/model).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `listing_id` | `string` | ✅ Yes | MongoDB ObjectId of the listing |

**Response:**

```json
{
  "listing_id": "6650af...",
  "predicted_price": 7420000.0,
  "actual_price": 6750000.0,
  "score": 0.9097,
  "label": "good_deal"
}
```

**Deal Labels:**

| Label | Condition | Meaning |
|---|---|---|
| `good_deal` | actual / predicted < 0.85 | Listed well below fair market value |
| `fair` | 0.85 ≤ ratio ≤ 1.15 | Priced around market average |
| `overpriced` | ratio > 1.15 | Listed above fair market value |
| `unknown` | actual price = 0 | Score could not be computed |

---

## Makes & Models

### `GET /api/v1/makes/`

Return all vehicle makes from the database (auto-seeded on startup from brand registry).

**Response:**

```json
{
  "makes": [
    { "name": "Toyota", "slug": "toyota", "scrape_url": "https://ikman.lk/en/ads/sri-lanka/cars/toyota?tree.brand=toyota" },
    { "name": "Honda", "slug": "honda", "scrape_url": "https://ikman.lk/en/ads/sri-lanka/cars/honda?tree.brand=honda" }
  ],
  "total": 56
}
```

---

### `GET /api/v1/makes/{make_name}/models`

Return all models for a make, with live listing counts.

**Response:**

```json
{
  "make": "toyota",
  "models": [
    { "name": "Aqua", "slug": "aqua", "scrape_url": "https://ikman.lk/.../aqua?tree.brand=toyota_toyota-aqua", "listing_count": 142 },
    { "name": "Prius", "slug": "prius", "scrape_url": "https://ikman.lk/.../prius?tree.brand=toyota_toyota-prius", "listing_count": 98 }
  ],
  "total": 68
}
```

---

### `GET /api/v1/makes/{make_name}/models/{model_name}/years`

Return year-by-year average price history for a make/model (uses PriceSnapshot aggregates).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `condition` | `string` | `null` | Filter by condition |

**Response:**

```json
{
  "make": "toyota",
  "model": "aqua",
  "condition": null,
  "data": [
    { "year": 2014, "avg_price": 5800000.0, "min_price": 4200000.0, "max_price": 7200000.0, "total_listings": 45 },
    { "year": 2015, "avg_price": 6500000.0, "min_price": 5000000.0, "max_price": 8100000.0, "total_listings": 62 }
  ]
}
```

---

## Search

### `GET /api/v1/search/`

Full-text search across vehicle listings (title, description, make, model, category, location).

| Parameter | Type | Default | Required | Description |
|---|---|---|---|---|
| `q` | `string` | — | ✅ Yes | Search query (min 1 char) |
| `page` | `int` | `1` | No | Page number (≥ 1) |
| `size` | `int` | `20` | No | Results per page (1–100) |

---

## Scraper

### `POST /api/v1/scrape/trigger`

Trigger a full market scrape (all brands → all models → all conditions). Runs in background.

**Response:**

```json
{
  "message": "Full market scrape started (all brands × all conditions)",
  "status": "running",
  "brands_count": 56
}
```

---

### `POST /api/v1/scrape/trigger/brand/{brand}`

Scrape a single brand across all its models and conditions. Runs in background.

---

### `GET /api/v1/scrape/brands`

Return the full list of supported brands and conditions.

---

### `GET /api/v1/scrape/status`

Return the result of the last scrape run.

---

## Logs

### WebSocket `/api/v1/logs/stream`
Stream logs from the backend directly to the client. Real-time updates push `{"message": "log trace", "level": "INFO|WARNING|ERROR"}` payload directly to any connected `WebSocket` subscribers instance.

---

## Schemas Reference

### Listing Schema

| Field | Type | Description |
|---|---|---|
| `id` | `string` | MongoDB ObjectId |
| `title` | `string` | Listing title |
| `description` | `string?` | Listing description |
| `price` | `float` | Price in LKR |
| `currency` | `string` | Currency code (default `"LKR"`) |
| `mileage` | `float?` | Mileage in km |
| `year` | `int?` | Year of manufacture |
| `location` | `string?` | Sri Lankan district |
| `source_url` | `string` | Original ikman.lk URL |
| `source_hash` | `string` | SHA-256 dedup hash |
| `make` | `string?` | Vehicle make (e.g. "Toyota") |
| `model` | `string?` | Vehicle model (e.g. "Aqua") |
| `condition` | `string?` | `used` / `brand_new` / `reconditioned` |
| `category` | `string?` | Vehicle category (e.g. "Cars") |
| `posted_date` | `string?` | Date ad was posted (ISO `YYYY-MM-DD`) |
| `created_at` | `datetime` | When scraped |
| `updated_at` | `datetime?` | Last update time |

---

### Make Schema

| Field | Type | Description |
|---|---|---|
| `name` | `string` | Display name (e.g. "Toyota") |
| `slug` | `string` | URL slug (e.g. "toyota") |
| `scrape_url` | `string` | ikman.lk scrape URL |

### Model Schema

| Field | Type | Description |
|---|---|---|
| `name` | `string` | Display name (e.g. "Aqua") |
| `slug` | `string` | URL slug (e.g. "aqua") |
| `make_slug` | `string` | Parent brand slug |
| `scrape_url` | `string` | ikman.lk model-level scrape URL |

---

### PriceSnapshot Schema (Daily Aggregate)

| Field | Type | Description |
|---|---|---|
| `snapshot_date` | `date` | Day of snapshot |
| `make` | `string` | Vehicle make |
| `model` | `string` | Vehicle model |
| `year` | `int?` | Manufacture year |
| `condition` | `string?` | Condition filter |
| `avg_price` | `float` | Average price in group |
| `min_price` | `float` | Lowest price |
| `max_price` | `float` | Highest price |
| `listing_count` | `int` | Listings in group |

---

### DailyAnalytics Schema

| Field | Type | Description |
|---|---|---|
| `date` | `string` | Snapshot date |
| `scope` | `string` | `"market"`, `"brand"`, or `"brand_condition"` |
| `brand` | `string?` | Brand name or null |
| `condition` | `string?` | Condition or null |
| `total_listings` | `int` | Active listings |
| `avg_price` | `float` | Average price |
| `min_price` | `float` | Lowest price |
| `max_price` | `float` | Highest price |
| `median_price` | `float` | Median price |
| `price_change_pct` | `float?` | % change vs previous day |

---

### DealScore Schema

| Field | Type | Description |
|---|---|---|
| `listing_id` | `string` | MongoDB ObjectId of scored listing |
| `predicted_price` | `float` | Predicted fair market price |
| `actual_price` | `float` | Actual listed price |
| `score` | `float` | Ratio (actual / predicted) |
| `label` | `string` | `good_deal` / `fair` / `overpriced` |

---

## Endpoint Summary

| Method | Path | Tag | Description |
|---|---|---|---|
| `GET` | `/health` | health | Health check |
| `GET` | `/api/v1/listings/` | listings | Paginated listings with filters |
| `GET` | `/api/v1/listings/{listing_id}` | listings | Single listing detail |
| `GET` | `/api/v1/analytics/avg-price` | analytics | Average price by make/model |
| `GET` | `/api/v1/analytics/trends` | analytics | Monthly price trends |
| `GET` | `/api/v1/analytics/summary` | analytics | Overall market summary |
| `GET` | `/api/v1/analytics/depreciation` | analytics | Depreciation curve |
| `GET` | `/api/v1/analytics/mileage` | analytics | Mileage curve |
| `GET` | `/api/v1/analytics/daily` | analytics | Latest market-wide snapshot |
| `GET` | `/api/v1/analytics/daily/brands` | analytics | Latest snapshot for all brands |
| `GET` | `/api/v1/analytics/daily/brand/{brand}` | analytics | Snapshot for specific brand |
| `GET` | `/api/v1/analytics/daily/brand/{brand}/{condition}` | analytics | Brand + condition snapshot |
| `GET` | `/api/v1/analytics/daily/history` | analytics | Historical daily snapshots |
| `GET` | `/api/v1/deals/score` | deals | Deal quality score |
| `GET` | `/api/v1/makes/` | makes | All vehicle makes (with scrape URLs) |
| `GET` | `/api/v1/makes/{name}/models` | makes | Models for a make (with listing counts) |
| `GET` | `/api/v1/makes/{make}/models/{model}/years` | makes | Year-by-year price history |
| `GET` | `/api/v1/search/` | search | Full-text search |
| `POST` | `/api/v1/scrape/trigger` | scrape | Trigger full market scrape |
| `POST` | `/api/v1/scrape/trigger/brand/{brand}` | scrape | Trigger single-brand scrape |
| `GET` | `/api/v1/scrape/status` | scrape | Last scrape result |
| `GET` | `/api/v1/scrape/brands` | scrape | List supported brands |
| `WS` | `/api/v1/logs/stream` | logs | Stream real-time backend logs via WebSocket |
