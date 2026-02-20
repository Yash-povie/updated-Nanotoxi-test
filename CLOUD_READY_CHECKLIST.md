# Cloud deployment checklist – NanoTox AI Backend

**Status: READY FOR CLOUD**

Run locally: `python check_analytics_ready.py` — all checks must pass before deploying.

---

## Analytics & dashboard (verified)

| Item | Status | Endpoint(s) |
|------|--------|-------------|
| Total predictions | OK | `GET /api/dashboard/stats` |
| Average response time | OK | `GET /api/dashboard/stats` |
| Predictions over time | OK | `GET /api/dashboard/predictions-over-time` |
| API uptime & health | OK | `GET /health` |
| Failed vs successful requests | OK | `GET /api/dashboard/request-stats` |
| Model load status | OK | `GET /health` (models_loaded, model_status) |
| Contact submissions | OK | `GET /api/dashboard/contact-requests` |
| Dataset-share submissions | OK | `GET /api/dashboard/dataset-requests` |
| Nanoparticle types (optional) | OK | `GET /api/dashboard/nanoparticle-types` |
| Recent predictions | OK | `GET /api/dashboard/recent-predictions` |
| Prediction history | OK | `GET /api/dashboard/prediction-history` |
| Toxicity distribution | OK | `GET /api/dashboard/toxicity-distribution` |

---

## Deployment config (verified)

| File | Purpose |
|------|---------|
| `railway.json` | Start: `gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app`, healthcheck: `/health` |
| `Procfile` | `web: gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 main:app` |
| `requirements.txt` | Flask, gunicorn, numpy 2.x, scikit-learn 1.7.1, flask-cors, ML libs |

---

## Before you deploy to cloud

1. **Commit everything**
   - `main.py` (dashboard + analytics)
   - `railway.json`, `Procfile`, `requirements.txt`
   - `DASHBOARD_API.md`, `check_analytics_ready.py`, `CLOUD_READY_CHECKLIST.md`
   - All `.pkl` model files

2. **Optional env vars (Railway dashboard)**
   - `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `ADMIN_EMAIL` (for contact/dataset emails)

3. **After deploy**
   - Test: `GET https://<your-app>.up.railway.app/health`
   - Test: `GET https://<your-app>.up.railway.app/api/dashboard/stats`
   - Point frontend dashboard to `https://<your-app>.up.railway.app` for all API and dashboard endpoints

---

## Note

Dashboard data (predictions, contacts, dataset requests) is **in-memory** and resets on each deploy or restart. For persistent analytics, add a database later and replace the in-memory lists in `main.py`.
