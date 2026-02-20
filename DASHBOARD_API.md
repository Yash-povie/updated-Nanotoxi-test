# Dashboard API – Endpoint reference

Base URL: `http://localhost:5000` (or your deployed URL).

All dashboard endpoints are **GET** and return JSON. Use them for KPI cards, charts, and tables in the frontend.

---

## 1. `GET /health`

**Use:** API uptime, health badge, model load status.

**Example response:**
```json
{
  "status": "healthy",
  "message": "NanoTox AI API is running",
  "timestamp": "2026-02-20T05:48:39.248271Z",
  "uptime_seconds": 95.8,
  "uptime_percentage": 100.0,
  "models_loaded": true,
  "model_status": "loaded"
}
```

- **Status badge:** `status` = `"healthy"`
- **Uptime gauge:** `uptime_seconds` (and optionally `uptime_percentage`)
- **Model indicator:** `models_loaded` (true/false), `model_status` (`"loaded"` or `"fallback"`)

---

## 2. `GET /api/dashboard/stats`

**Use:** Total predictions (KPI), average response time (KPI), success/fail counts.

**Example response:**
```json
{
  "total_predictions": 3,
  "average_response_time_ms": 0.58,
  "prediction_success_count": 3,
  "prediction_fail_count": 0
}
```

- **KPI – Total predictions:** `total_predictions`
- **KPI – Avg response time:** `average_response_time_ms` (ms)

---

## 3. `GET /api/dashboard/predictions-over-time`

**Use:** Line chart or bar chart of predictions per day (and toxic vs non-toxic).

**Example response:**
```json
{
  "series": [
    {
      "date": "2026-02-20",
      "total": 3,
      "toxic": 2,
      "non_toxic": 1
    }
  ]
}
```

- **X-axis:** `date`
- **Y-axis:** `total`, or stacked `toxic` / `non_toxic`

---

## 4. `GET /api/dashboard/request-stats`

**Use:** Pie or donut chart: successful vs failed prediction requests.

**Example response:**
```json
{
  "success": 3,
  "failed": 0,
  "total": 3
}
```

---

## 5. `GET /api/dashboard/toxicity-distribution`

**Use:** Pie or bar chart: toxic vs non-toxic outcomes.

**Example response:**
```json
{
  "toxic": 2,
  "non_toxic": 1,
  "total": 3
}
```

---

## 6. `GET /api/dashboard/contact-requests`

**Use:** Table of contact form submissions.

**Example response:**
```json
{
  "requests": [
    {
      "timestamp": "2026-02-20T05:48:20.391438Z",
      "name": "Demo User",
      "email": "demo@test.com",
      "profession": "",
      "phone": "",
      "message": "Test message"
    }
  ]
}
```

- Newest first. Render as table columns: timestamp, name, email, profession, phone, message.

---

## 7. `GET /api/dashboard/dataset-requests`

**Use:** Table of dataset sharing submissions.

**Example response:**
```json
{
  "requests": [
    {
      "timestamp": "2026-02-20T05:48:20.395139Z",
      "name": "Lab A",
      "email": "lab@test.com",
      "organization": "",
      "dataset_description": "Sample dataset",
      "dataset_size": "",
      "research_area": ""
    }
  ]
}
```

- Newest first. Table columns: timestamp, name, email, organization, dataset_description, dataset_size, research_area.

---

## 8. `GET /api/dashboard/nanoparticle-types`

**Use:** Bar chart of most common nanoparticle types (by count).

**Example response:**
```json
{
  "series": [
    { "nanoparticle_id": "CuO_30nm", "count": 1 },
    { "nanoparticle_id": "SiO2_50nm", "count": 1 },
    { "nanoparticle_id": "ZnO_25nm", "count": 1 }
  ]
}
```

- Sorted by count descending. X-axis: `nanoparticle_id`, Y-axis: `count`.

---

## 9. `GET /api/dashboard/recent-predictions`

**Use:** Table of latest predictions and toxicity KPI.

**Query:** `?limit=20` (default 20, max 100).

**Example response:**
```json
{
  "predictions": [
    {
      "timestamp": "2026-02-20T05:48:20.387445Z",
      "nanoparticle_id": "ZnO_25nm",
      "toxicity": "TOXIC",
      "confidence": 0.91,
      "cytotoxicity": "YES",
      "response_time_ms": 0.17,
      "risk_level": "HIGH RISK - Immediate concern",
      "key_factors": {
        "material": "80.0%",
        "size_effect": "HIGH",
        "surface_reactivity": "HIGH",
        "environmental": "FAVORABLE"
      }
    }
  ]
}
```

- **Toxicity outcome:** use `toxicity`, `confidence`, `cytotoxicity`, `risk_level`.
- **Contributing factors:** use `key_factors` for tooltips or detail panel.

---

## 10. `GET /api/dashboard/prediction-history`

**Use:** Paginated table (and detail panel) of full prediction history.

**Query:** `?limit=50&offset=0` (default limit 50, max 200).

**Example response:**
```json
{
  "predictions": [ /* same shape as recent-predictions */ ],
  "total": 3,
  "offset": 0,
  "limit": 5
}
```

- **Table:** `predictions[]` with columns as in recent-predictions.
- **Pagination:** use `total`, `offset`, `limit`.
- **Confidence / key factors:** same as `/api/dashboard/recent-predictions` (or from `/predict` response).

---

## Quick mapping to UI

| UI element              | Endpoint                              |
|-------------------------|----------------------------------------|
| Total predictions       | `/api/dashboard/stats` → `total_predictions` |
| Predictions over time   | `/api/dashboard/predictions-over-time` |
| Uptime / health         | `/health` → `uptime_seconds`, `status` |
| Failed vs success       | `/api/dashboard/request-stats`         |
| Model status            | `/health` → `models_loaded`           |
| Avg response time       | `/api/dashboard/stats` → `average_response_time_ms` |
| Contact submissions     | `/api/dashboard/contact-requests`     |
| Dataset submissions     | `/api/dashboard/dataset-requests`     |
| Nanoparticle types      | `/api/dashboard/nanoparticle-types`   |
| Recent predictions      | `/api/dashboard/recent-predictions`   |
| Prediction history      | `/api/dashboard/prediction-history`   |
| Toxicity distribution  | `/api/dashboard/toxicity-distribution` |

Data is stored in memory and resets on server restart. For persistence, add a database and replace the in-memory stores in `main.py`.
