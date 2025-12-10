import requests
import json

url = "http://127.0.0.1:8000/query"
payload = {"query": "how to groupby and aggregate in pandas", "top_k": 3}

resp = requests.post(url, json=payload)
print("Status:", resp.status_code)
print(json.dumps(resp.json(), indent=2)[:4000])
