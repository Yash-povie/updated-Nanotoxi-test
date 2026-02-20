#!/usr/bin/env python3
"""
DEMO: See the real working of the API and analytics.
Run this while the server is running (python main.py).
Shows BEFORE → action → AFTER so you see how data flows into the dashboard.
"""
import urllib.request
import json
import time

BASE = "http://127.0.0.1:5000"

def get(path):
    req = urllib.request.Request(BASE + path)
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode())

def post(path, data):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode())

def main():
    print("=" * 60)
    print("  NANOTOX AI – REAL WORKING DEMO")
    print("  (Server must be running: python main.py)")
    print("=" * 60)

    # ---------- BEFORE: show current dashboard state ----------
    print("\n--- BEFORE (current dashboard state) ---\n")
    stats = get("/api/dashboard/stats")
    dist = get("/api/dashboard/toxicity-distribution")
    req_stats = get("/api/dashboard/request-stats")
    recent = get("/api/dashboard/recent-predictions")
    over_time = get("/api/dashboard/predictions-over-time")

    print("  /api/dashboard/stats:")
    print(f"    total_predictions     = {stats['total_predictions']}")
    print(f"    average_response_time_ms = {stats['average_response_time_ms']}")
    print(f"    prediction_success_count = {stats['prediction_success_count']}")
    print()
    print("  /api/dashboard/request-stats (for pie chart):")
    print(f"    success = {req_stats['success']}, failed = {req_stats['failed']}, total = {req_stats['total']}")
    print()
    print("  /api/dashboard/toxicity-distribution (for pie/bar):")
    print(f"    toxic = {dist['toxic']}, non_toxic = {dist['non_toxic']}, total = {dist['total']}")
    print()
    print("  /api/dashboard/recent-predictions:")
    print(f"    number of rows = {len(recent['predictions'])}")
    if recent["predictions"]:
        p = recent["predictions"][0]
        print(f"    latest: {p['nanoparticle_id']} -> {p['toxicity']} (confidence {p.get('confidence')})")
    print()
    print("  /api/dashboard/predictions-over-time:")
    print(f"    series (by date) = {over_time['series']}")
    print()

    # ---------- ACTION 1: Run a prediction ----------
    print("--- ACTION 1: POST /predict (CuO nanoparticle) ---\n")
    payload = {
        "nanoparticle_id": "CuO_30nm_demo",
        "core_size": 30.0,
        "zeta_potential": -28.0,
        "surface_area": 95.0,
        "bandgap_energy": 1.2,
        "electric_charge": -1,
        "oxygen_atoms": 1,
        "dosage": 40.0,
        "exposure_time": 24.0,
        "environmental_pH": 6.5,
        "protein_corona": False,
    }
    resp = post("/predict", payload)
    print("  Response from /predict:")
    print(f"    success = {resp.get('success')}")
    print(f"    nanoparticle_id = {resp.get('nanoparticle_id')}")
    print(f"    toxicity = {resp['stage2']['toxicity_prediction']}")
    print(f"    confidence = {resp['stage2']['confidence']}")
    print(f"    cytotoxicity = {resp['stage3']['cytotoxicity']}")
    print()

    # ---------- AFTER ACTION 1: show dashboard again ----------
    print("--- AFTER ACTION 1: dashboard updated ---\n")
    stats = get("/api/dashboard/stats")
    dist = get("/api/dashboard/toxicity-distribution")
    recent = get("/api/dashboard/recent-predictions")
    over_time = get("/api/dashboard/predictions-over-time")
    print("  /api/dashboard/stats:")
    print(f"    total_predictions     = {stats['total_predictions']}  (incremented by 1)")
    print(f"    average_response_time_ms = {stats['average_response_time_ms']}  (from this request)")
    print()
    print("  /api/dashboard/toxicity-distribution:")
    print(f"    toxic = {dist['toxic']}, non_toxic = {dist['non_toxic']}  (updated from prediction)")
    print()
    print("  /api/dashboard/recent-predictions (latest row):")
    if recent["predictions"]:
        p = recent["predictions"][0]
        print(f"    timestamp = {p['timestamp']}")
        print(f"    nanoparticle_id = {p['nanoparticle_id']}, toxicity = {p['toxicity']}")
        print(f"    response_time_ms = {p['response_time_ms']}, key_factors = {p.get('key_factors')}")
    print()
    print("  /api/dashboard/predictions-over-time:")
    print(f"    series = {over_time['series']}  (one day with total/toxic/non_toxic)")
    print()

    # ---------- ACTION 2: Another prediction (SiO2 – non-toxic) ----------
    print("--- ACTION 2: POST /predict (SiO2 – usually non-toxic) ---\n")
    payload2 = {
        "nanoparticle_id": "SiO2_50nm_demo",
        "core_size": 50.0,
        "zeta_potential": -35.0,
        "surface_area": 80.0,
        "bandgap_energy": 9.0,
        "electric_charge": -1,
        "oxygen_atoms": 2,
        "dosage": 20.0,
        "exposure_time": 24.0,
        "environmental_pH": 7.0,
        "protein_corona": False,
    }
    resp2 = post("/predict", payload2)
    print(f"  toxicity = {resp2['stage2']['toxicity_prediction']}, confidence = {resp2['stage2']['confidence']}")
    print()

    # ---------- ACTION 3: Contact form ----------
    print("--- ACTION 3: POST /contact ---\n")
    contact_resp = post("/contact", {
        "name": "Demo User",
        "email": "demo@example.com",
        "message": "I want to see how the dashboard gets this submission.",
    })
    print(f"  success = {contact_resp.get('success')}, message = {contact_resp.get('message')}")
    print()

    # ---------- ACTION 4: Dataset share ----------
    print("--- ACTION 4: POST /share-dataset ---\n")
    share_resp = post("/share-dataset", {
        "name": "Demo Lab",
        "email": "lab@example.com",
        "dataset_description": "Demo dataset to show dashboard table.",
    })
    print(f"  success = {share_resp.get('success')}")
    print()

    # ---------- FINAL STATE: all dashboard endpoints with real data ----------
    print("--- FINAL STATE: all analytics with real data ---\n")
    stats = get("/api/dashboard/stats")
    dist = get("/api/dashboard/toxicity-distribution")
    req_stats = get("/api/dashboard/request-stats")
    recent = get("/api/dashboard/recent-predictions")
    over_time = get("/api/dashboard/predictions-over-time")
    nano_types = get("/api/dashboard/nanoparticle-types")
    contacts = get("/api/dashboard/contact-requests")
    datasets = get("/api/dashboard/dataset-requests")
    health = get("/health")

    print("  1. /health (uptime, model status):")
    print(f"     uptime_seconds = {health['uptime_seconds']}, models_loaded = {health['models_loaded']}")
    print()
    print("  2. /api/dashboard/stats (KPI cards):")
    print(f"     total_predictions = {stats['total_predictions']}")
    print(f"     average_response_time_ms = {stats['average_response_time_ms']}")
    print()
    print("  3. /api/dashboard/request-stats (pie: success vs failed):")
    print(f"     success = {req_stats['success']}, failed = {req_stats['failed']}")
    print()
    print("  4. /api/dashboard/toxicity-distribution (pie/bar: toxic vs non_toxic):")
    print(f"     toxic = {dist['toxic']}, non_toxic = {dist['non_toxic']}")
    print()
    print("  5. /api/dashboard/predictions-over-time (line/bar by date):")
    for s in over_time["series"]:
        print(f"     date {s['date']}: total={s['total']}, toxic={s['toxic']}, non_toxic={s['non_toxic']}")
    print()
    print("  6. /api/dashboard/nanoparticle-types (bar chart):")
    for t in nano_types["series"]:
        print(f"     {t['nanoparticle_id']}: count = {t['count']}")
    print()
    print("  7. /api/dashboard/recent-predictions (table):")
    for p in recent["predictions"][:3]:
        print(f"     {p['timestamp'][:19]} | {p['nanoparticle_id']} | {p['toxicity']} | {p['response_time_ms']} ms")
    print()
    print("  8. /api/dashboard/contact-requests (table):")
    for c in contacts["requests"][:2]:
        print(f"     {c['timestamp'][:19]} | {c['name']} | {c['email']} | {c['message'][:40]}...")
    print()
    print("  9. /api/dashboard/dataset-requests (table):")
    for d in datasets["requests"][:2]:
        print(f"     {d['timestamp'][:19]} | {d['name']} | {d['email']} | {d['dataset_description'][:40]}...")
    print()
    print("=" * 60)
    print("  This is the real working: each POST updated the in-memory")
    print("  store, and every GET reads from it. Your frontend dashboard")
    print("  calls these same endpoints to show charts and tables.")
    print("=" * 60)

if __name__ == "__main__":
    main()
