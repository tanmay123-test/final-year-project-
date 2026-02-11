import requests

API = "http://127.0.0.1:5000"

try:
    r = requests.get(f"{API}/admin/workers/pending")
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
    if r.status_code == 200:
        print("✅ JSON Decode Success:", r.json())
    else:
        print("❌ Request failed")
except Exception as e:
    print(f"❌ Exception: {e}")
