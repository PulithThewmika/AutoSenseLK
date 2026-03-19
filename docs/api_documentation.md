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
- [Schemas Reference](#schemas-reference)

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
| `make` | `string` | `null` | Filter by vehicle make |
| `model` | `string` | `null` | Filter by vehicle model |
| `min_price` | `float` | `null` | Minimum price (LKR) |
| `max_price` | `float` | `null` | Maximum price (LKR) |
| `year_from` | `int` | `null` | Minimum manufacturing year |
| `year_to` | `int` | `null` | Maximum manufacturing year |

**Example Request:**

```
GET /api/v1/listings/?page=1&size=10&make=Toyota&min_price=5000000&year_from=2015
```

**Response Schema:** `ListingListResponse`

```json
{
  "page": 1,
  "size": 10,
  "total": 142,
  "results": [
    {
      "id": 1,
      "title": "Toyota Aqua S 2016",
      "price": 7680000.0,
      "currency": "LKR",
      "mileage": 68000.0,
      "year": 2016,
      "location": "Colombo",
      "source_url": "https://ikman.lk/en/ad/...",
      "make_id": 1,
      "model_id": 5,
      "created_at": "2026-03-15T12:00:00Z"
    }
  ]
}
```

---

### `GET /api/v1/listings/{listing_id}`

Return a single listing by its ID.

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `listing_id` | `int` | Unique listing identifier |

**Response:**

```json
{
  "listing_id": 42
}
```

---

## Analytics

### `GET /api/v1/analytics/avg-price`

Return the average price across listings, optionally filtered by make and/or model.

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | `string` | `null` | Filter by make name |
| `model` | `string` | `null` | Filter by model name |

**Response Schema:** `AvgPriceResponse`

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

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `make` | `string` | `null` | Filter by make name |
| `model` | `string` | `null` | Filter by model name |
| `months` | `int` | `12` | Number of months of history (1–60) |

**Response Schema:** `PriceTrendResponse`

```json
{
  "make": "Toyota",
  "model": "Aqua",
  "trends": [
    { "month": "2026-01", "avg_price": 7350000.0, "count": 28 },
    { "month": "2026-02", "avg_price": 7500000.0, "count": 31 }
  ]
}
```

---

### `GET /api/v1/analytics/summary`

Return overall market statistics including total listings, average price, and counts of unique makes/models.

---

### `GET /api/v1/analytics/depreciation`

Return price-vs-year depreciation curve.

---

### `GET /api/v1/analytics/mileage`

Return price-vs-mileage curve bucketed by 25,000 km bands.

---

### `GET /api/v1/analytics/daily`

Return the latest market-wide daily analytics snapshot.

---

### `GET /api/v1/analytics/daily/brands`

Return the latest daily snapshot for every brand.

---

### `GET /api/v1/analytics/daily/brand/{brand}`

Return the latest daily snapshot for a specific brand (with condition breakdown).

---

### `GET /api/v1/analytics/daily/history`

Return historical daily analytics snapshots.

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `days` | `int` | `30` | Number of days |
| `scope` | `string` | `"market"` | `"market"`, `"brand"`, or `"brand_condition"` |
| `brand` | `string` | `null` | Filter by brand (optional) |

---

## Deal Scoring

### `GET /api/v1/deals/score`

Return the ML-generated deal score for a specific listing. Compares the listing's actual price against the model-predicted fair price.

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `listing_id` | `int` | ✅ Yes | ID of the listing to score |

**Response Schema:** `DealScoreResponse`

```json
{
  "listing_id": 42,
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

Return all known vehicle makes (manufacturers).

**Response:**

```json
{
  "makes": [
    { "id": "abc123", "name": "Toyota" },
    { "id": "def456", "name": "Honda" },
    { "id": "ghi789", "name": "Suzuki" }
  ]
}
```

---

### `GET /api/v1/makes/{make_id}/models`

Return all models belonging to a specific make.

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `make_id` | `int` | ID of the vehicle make |

**Response:**

```json
{
  "make_id": 1,
  "models": [
    { "id": "m001", "name": "Aqua", "make_id": "abc123" },
    { "id": "m002", "name": "Prius", "make_id": "abc123" }
  ]
}
```

---

## Search

### `GET /api/v1/search/`

Full-text search across all vehicle listings.

**Query Parameters:**

| Parameter | Type | Default | Required | Description |
|---|---|---|---|---|
| `q` | `string` | — | ✅ Yes | Search query (min 1 char, searches across title, description, make, model, category, and location) |
| `page` | `int` | `1` | No | Page number (≥ 1) |
| `size` | `int` | `20` | No | Results per page (1–100) |

**Example Request:**

```
GET /api/v1/search/?q=toyota+aqua&page=1&size=10
```

**Response:**

```json
{
  "query": "toyota aqua",
  "page": 1,
  "size": 10,
  "results": []
}
```

---

## Scraper

### `POST /api/v1/scrape/trigger`

Manually trigger a full market scrape cycle (all brands × all conditions). The scrape runs in the background and returns immediately.

**Response:**

```json
{
  "message": "Full market scrape started (all brands × all conditions)",
  "status": "running",
  "brands_count": 55
}
```

---

### `POST /api/v1/scrape/trigger/brand/{brand}`

Scrape a single brand across all conditions on-demand. Returns immediately.

---

### `GET /api/v1/scrape/brands`

Return the list of all 55+ supported brands and conditions.

---

### `GET /api/v1/scrape/status`

Return the result of the last scrape run.

**Response (no runs yet):**

```json
{
  "status": "no_runs_yet"
}
```

**Response (completed):**

```json
{
  "status": "completed",
  "total_found": 120,
  "new_listings": 85,
  "duplicates_skipped": 35,
  "saved": 85
}
```

**Response (failed):**

```json
{
  "status": "failed",
  "error": "Error description"
}
```

---

## Schemas Reference

### Listing Schemas

#### `ListingBase`

| Field | Type | Default | Description |
|---|---|---|---|
| `title` | `string` | — | Listing title |
| `price` | `float` | — | Price in LKR |
| `currency` | `string` | `"LKR"` | Currency code |
| `mileage` | `float?` | `null` | Mileage in km |
| `year` | `int?` | `null` | Year of manufacture |
| `location` | `string?` | `null` | Sri Lankan district |

#### `ListingCreate` (extends ListingBase)

| Field | Type | Description |
|---|---|---|
| `source_url` | `HttpUrl` | URL of the original listing |
| `make_id` | `int?` | Reference to make |
| `model_id` | `int?` | Reference to model |

#### `ListingResponse` (extends ListingBase)

| Field | Type | Description |
|---|---|---|
| `id` | `int` | Unique listing ID |
| `source_url` | `string` | Original listing URL |
| `make_id` | `int?` | Reference to make |
| `model_id` | `int?` | Reference to model |
| `created_at` | `datetime?` | Timestamp of creation |

#### `ListingListResponse`

| Field | Type | Description |
|---|---|---|
| `page` | `int` | Current page |
| `size` | `int` | Page size |
| `total` | `int` | Total matching listings |
| `results` | `ListingResponse[]` | Array of listings |

---

### Analytics Schemas

#### `AvgPriceResponse`

| Field | Type | Description |
|---|---|---|
| `make` | `string?` | Make filter used |
| `model` | `string?` | Model filter used |
| `avg_price` | `float` | Computed average price |
| `sample_count` | `int` | Number of listings sampled |

#### `PriceTrendPoint`

| Field | Type | Description |
|---|---|---|
| `month` | `string` | Month label (e.g. `"2026-01"`) |
| `avg_price` | `float` | Average price for the month |
| `count` | `int` | Number of listings in that month |

#### `PriceTrendResponse`

| Field | Type | Description |
|---|---|---|
| `make` | `string?` | Make filter used |
| `model` | `string?` | Model filter used |
| `trends` | `PriceTrendPoint[]` | Array of monthly data points |

#### `DailyAnalyticsResponse`

| Field | Type | Description |
|---|---|---|
| `date` | `string` | Snapshot date (e.g. "2026-03-19") |
| `scope` | `string` | `"market"`, `"brand"`, or `"brand_condition"` |
| `brand` | `string?` | Brand name or null |
| `condition` | `string?` | Condition (used, brand_new...) or null |
| `total_listings` | `int` | Number of active listings |
| `avg_price` | `float` | Average listed price |
| `min_price` | `float` | Lowest listed price |
| `max_price` | `float` | Highest listed price |
| `median_price` | `float` | Median listed price |
| `price_change_pct` | `float?` | Change from previous day |


---

### Deal Schema

#### `DealScoreResponse`

| Field | Type | Description |
|---|---|---|
| `listing_id` | `int` | Listing that was scored |
| `predicted_price` | `float` | ML-predicted fair market price |
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
| `GET` | `/api/v1/analytics/daily/history` | analytics | Historical daily snapshots |
| `GET` | `/api/v1/deals/score` | deals | ML deal quality score |
| `GET` | `/api/v1/makes/` | makes | All vehicle makes |
| `GET` | `/api/v1/makes/{make_id}/models` | makes | Models for a make |
| `GET` | `/api/v1/search/` | search | Full-text search |
| `POST` | `/api/v1/scrape/trigger` | scrape | Trigger full market scrape |
| `POST` | `/api/v1/scrape/trigger/brand/{brand}` | scrape | Trigger single-brand scrape |
| `GET` | `/api/v1/scrape/status` | scrape | Last scrape result |
| `GET` | `/api/v1/scrape/brands` | scrape | List supported brands |
