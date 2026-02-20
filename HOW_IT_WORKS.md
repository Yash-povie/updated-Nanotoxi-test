# How the NanoTox AI backend and analytics work

A walkthrough with a **real example** so you can see the flow end-to-end.

---

## 1. When a prediction runs (`POST /predict`)

**What the frontend sends:**
```json
POST /predict
{
  "nanoparticle_id": "CuO_30nm",
  "core_size": 30,
  "zeta_potential": -28,
  "surface_area": 95,
  "dosage": 40,
  "exposure_time": 24,
  "environmental_pH": 6.5,
  "protein_corona": false,
  ...
}
```

**What happens inside the backend:**

1. **Before the request**  
   `@app.before_request` runs and stores **start time** (`g.start_time = time.time()`).

2. **Your app logic**  
   - Stage 1: aggregation (hydrodynamic diameter, stability).  
   - Stage 2: toxicity (TOXIC / NON-TOXIC, confidence, risk level).  
   - Stage 3: cytotoxicity (YES / NO).  
   - Key factors (material %, size, surface, environment) are computed.

3. **Logging for the dashboard**  
   Before returning the response, the app appends **one record** to an in-memory list:
   - `timestamp`, `nanoparticle_id`, `toxicity`, `confidence`, `cytotoxicity`, `response_time_ms`, `key_factors`, `risk_level`.

4. **After the request**  
   `@app.after_request` runs only for `/predict`:  
   - If status is success (2xx): increment **success count** and append **response time** to a list (for “average response time”).  
   - If status is error (4xx/5xx): increment **fail count**.

5. **Response to the frontend**  
   The usual prediction JSON (stage1, stage2, stage3, key_factors, etc.) is returned.

So: **one prediction request** → **one new row** in the prediction log and **one update** to success/fail and response-time stats.

---

## 2. Where that data is used (dashboard endpoints)

All dashboard endpoints **read from the same in-memory data** that was just updated.

| Dashboard need | Where data comes from | Endpoint |
|----------------|------------------------|----------|
| **Total predictions** | Number of records in the prediction log | `GET /api/dashboard/stats` → `total_predictions` |
| **Average response time** | Average of last 500 `/predict` response times (ms) | `GET /api/dashboard/stats` → `average_response_time_ms` |
| **Success vs failed** | Counters incremented in `after_request` for `/predict` | `GET /api/dashboard/request-stats` → `success`, `failed` |
| **Predictions over time** | Prediction log grouped by **date** (total, toxic, non_toxic per day) | `GET /api/dashboard/predictions-over-time` → `series[]` |
| **Toxicity distribution** | Prediction log: count where toxicity = TOXIC vs NON-TOXIC | `GET /api/dashboard/toxicity-distribution` → `toxic`, `non_toxic` |
| **Recent predictions** | Last N records from the prediction log (newest first) | `GET /api/dashboard/recent-predictions?limit=20` → `predictions[]` |
| **Prediction history** | Same log, paginated (offset + limit) | `GET /api/dashboard/prediction-history?limit=50&offset=0` → `predictions[]`, `total` |
| **Most common nanoparticle types** | Prediction log: count by `nanoparticle_id` | `GET /api/dashboard/nanoparticle-types` → `series[]` (nanoparticle_id, count) |

So when you “see the real working”, you’re seeing:  
**real requests** → **same data** → **different dashboard endpoints** that slice that data in different ways (totals, time series, tables, distributions).

---

## 3. Contact and dataset-share (same idea)

- **`POST /contact`**  
  When the request is valid and the handler returns success, the app appends one record to the **contact list** (timestamp, name, email, profession, phone, message).  
  **Dashboard:** `GET /api/dashboard/contact-requests` returns that list (newest first).

- **`POST /share-dataset`**  
  Same idea: on success, one record is appended (timestamp, name, email, organization, dataset_description, etc.).  
  **Dashboard:** `GET /api/dashboard/dataset-requests` returns that list.

So: **one form submit** → **one new row** in the corresponding list → **table endpoint** shows it.

---

## 4. Health and uptime (no “logging”, just current state)

- **`GET /health`**  
  Does **not** read from the prediction/contact logs. It computes **once per request**:
  - **Uptime:** `now - APP_START_TIME` (when the process started).
  - **Model status:** whether the ML models were loaded at startup (`models_loaded`, `model_status`).

So “how it works” for health: **each request** → **current uptime and model status** → returned as JSON for status badge / gauge.

---

## 5. End-to-end example (what you actually see)

**Step 1 – Before any predictions**  
- `GET /api/dashboard/stats` → `total_predictions: 0`, `average_response_time_ms: 0`.  
- `GET /api/dashboard/recent-predictions` → `predictions: []`.  
- `GET /api/dashboard/toxicity-distribution` → `toxic: 0`, `non_toxic: 0`.

**Step 2 – You run 1 prediction (e.g. CuO)**  
- `POST /predict` with CuO payload → response 200, body has `toxicity: "TOXIC"`, etc.  
- Internally: one record appended to prediction log; success count +1; one response time stored.

**Step 3 – Right after that**  
- `GET /api/dashboard/stats` → `total_predictions: 1`, `average_response_time_ms: 0.85` (or similar).  
- `GET /api/dashboard/recent-predictions` → `predictions: [ { nanoparticle_id: "CuO_30nm", toxicity: "TOXIC", ... } ]`.  
- `GET /api/dashboard/toxicity-distribution` → `toxic: 1`, `non_toxic: 0`, `total: 1`.  
- `GET /api/dashboard/predictions-over-time` → one day with `total: 1`, `toxic: 1`, `non_toxic: 0`.

**Step 4 – You run 2 more (e.g. SiO2, ZnO)**  
- Same flow: 2 more rows in the log, 2 more success counts, 2 more response times.  
- Now:  
  - `total_predictions: 3`,  
  - `recent-predictions` has 3 items (newest first),  
  - `toxicity-distribution` reflects 2 toxic + 1 non-toxic (or whatever the model returned),  
  - `predictions-over-time` still one day with `total: 3`, `toxic: 2`, `non_toxic: 1`.

That’s the **real working**: every real prediction/contact/dataset request updates the in-memory data, and the dashboard endpoints just **read** that same data in different ways. Running the demo script (below) replays this so you can see the numbers change live.
