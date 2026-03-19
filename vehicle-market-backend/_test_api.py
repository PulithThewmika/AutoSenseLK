"""Quick API verification script."""
import httpx
import json

BASE = "http://localhost:8000"

endpoints = [
    ("Health", "/health"),
    ("Avg Price", "/api/v1/analytics/avg-price"),
    ("Summary", "/api/v1/analytics/summary"),
    ("Makes", "/api/v1/makes/"),
    ("Search toyota", "/api/v1/search/?q=toyota"),
    ("Trends", "/api/v1/analytics/trends?months=6"),
]

for name, path in endpoints:
    try:
        r = httpx.get(BASE + path, timeout=10)
        data = r.json()
        print(f"OK {name} ({r.status_code})")
        print(f"  {json.dumps(data, default=str)[:300]}")
        print()
    except Exception as e:
        print(f"FAIL {name}: {e}")
        print()
