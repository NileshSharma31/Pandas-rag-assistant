import requests, time, json
from pathlib import Path

OUT = Path("data/so")
OUT.mkdir(parents=True, exist_ok=True)

API = "https://api.stackexchange.com/2.3/questions"
params = {
    "order":"desc",
    "sort":"votes",
    "tagged":"pandas",
    "site":"stackoverflow",
    "filter":"withbody",
    "pagesize":100
}

def fetch_pages(pages=3):
    all_qs=[]
    for page in range(1, pages+1):
        params["page"]=page
        r=requests.get(API, params=params)
        r.raise_for_status()
        data=r.json()
        all_qs.extend(data.get("items",[]))
        print(f"Fetched page {page} -> total {len(all_qs)}")
        time.sleep(1.2)
    return all_qs

if __name__=="__main__":
    qs = fetch_pages(pages=3)
    out_file = OUT / "so_pandas_top.json"
    out_file.write_text(json.dumps(qs, indent=2))
    print("Saved:", out_file)
