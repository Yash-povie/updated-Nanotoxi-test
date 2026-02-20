#!/usr/bin/env python3
"""Check all analytics/dashboard endpoints and deployment readiness."""
import urllib.request
import urllib.error
import json
import sys

BASE = "http://127.0.0.1:5000"
TIMEOUT = 5

def get(url):
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode() if e.fp else ""
    except Exception as e:
        return None, str(e)

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST",
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode() if e.fp else ""
    except Exception as e:
        return None, str(e)

def main():
    ok = 0
    fail = 0

    # Core + health
    for path in ["/", "/health", "/healthz", "/ping"]:
        status, body = get(BASE + path)
        if status == 200:
            print(f"  OK  GET {path}")
            ok += 1
            if path == "/health" and body:
                d = json.loads(body)
                if "uptime_seconds" in d and "models_loaded" in d:
                    print(f"       -> uptime_seconds, models_loaded present")
        else:
            print(f"  FAIL GET {path} -> {status} {body[:80]}")
            fail += 1

    # Dashboard endpoints (all GET)
    dashboard_paths = [
        "/api/dashboard/stats",
        "/api/dashboard/predictions-over-time",
        "/api/dashboard/request-stats",
        "/api/dashboard/toxicity-distribution",
        "/api/dashboard/contact-requests",
        "/api/dashboard/dataset-requests",
        "/api/dashboard/nanoparticle-types",
        "/api/dashboard/recent-predictions",
        "/api/dashboard/prediction-history",
    ]
    for path in dashboard_paths:
        status, body = get(BASE + path)
        if status == 200:
            try:
                d = json.loads(body)
                print(f"  OK  GET {path}")
                ok += 1
            except json.JSONDecodeError:
                print(f"  FAIL GET {path} -> invalid JSON")
                fail += 1
        else:
            print(f"  FAIL GET {path} -> {status}")
            fail += 1

    # Seed one prediction and verify dashboard updates
    payload = {
        "nanoparticle_id": "Check_CuO",
        "core_size": 30,
        "zeta_potential": -28,
        "surface_area": 95,
        "bandgap_energy": 1.2,
        "electric_charge": -1,
        "oxygen_atoms": 1,
        "dosage": 40,
        "exposure_time": 24,
        "environmental_pH": 6.5,
        "protein_corona": False,
    }
    status, body = post(BASE + "/predict", payload)
    if status == 200:
        print(f"  OK  POST /predict (seed)")
        ok += 1
    else:
        print(f"  FAIL POST /predict -> {status}")
        fail += 1

    # Re-check stats and toxicity after seed
    status, body = get(BASE + "/api/dashboard/stats")
    if status == 200:
        d = json.loads(body)
        if d.get("total_predictions", 0) >= 1 and "average_response_time_ms" in d:
            print(f"  OK  Dashboard stats updated (total_predictions, average_response_time_ms)")
            ok += 1
        else:
            print(f"  FAIL Dashboard stats missing fields or not updated")
            fail += 1
    else:
        fail += 1

    status, body = get(BASE + "/api/dashboard/toxicity-distribution")
    if status == 200:
        d = json.loads(body)
        if "toxic" in d and "non_toxic" in d:
            print(f"  OK  Toxicity distribution has toxic/non_toxic")
            ok += 1
        else:
            fail += 1
    else:
        fail += 1

    # Summary
    print()
    print("=" * 50)
    if fail == 0:
        print("RESULT: All analytics checks PASSED. Ready for cloud.")
        print("=" * 50)
        return 0
    else:
        print(f"RESULT: {fail} check(s) FAILED. Fix before deploying.")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
