# scripts/fetch_so_answers.py
import json, requests, time
from pathlib import Path

sofile = Path("data/so/so_pandas_top.json")
out = Path("data/so/answers")
out.mkdir(parents=True, exist_ok=True)

if not sofile.exists():
    raise SystemExit("Error: data/so/so_pandas_top.json not found. Run fetch_so_pandas.py first.")

data = json.loads(sofile.read_text())

API_BASE = "https://api.stackexchange.com/2.3/questions/{qid}/answers"
# polite pause between requests
SLEEP_BETWEEN = 1.2
# how many retries for transient errors (429, 502, 503, 504)
RETRIES = 3

def fetch_answers_for_q(qid):
    url = API_BASE.format(qid=qid)
    params = {
        "site": "stackoverflow",
        "filter": "withbody",
        "pagesize": 100,
        "order": "desc",
        "sort": "votes"
    }
    for attempt in range(1, RETRIES+1):
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json().get("items", [])
            # treat 4xx (other than 429) as non-retryable
            if 400 <= r.status_code < 500 and r.status_code != 429:
                print(f"[{qid}] Non-retryable HTTP {r.status_code} — skipping.")
                return None
            # for retryable codes, fall through to retry logic
            print(f"[{qid}] HTTP {r.status_code} on attempt {attempt}. Retrying after backoff.")
        except requests.RequestException as e:
            print(f"[{qid}] Request exception on attempt {attempt}: {e}")
        time.sleep(2 ** attempt)  # exponential backoff
    print(f"[{qid}] Failed after {RETRIES} attempts — skipping.")
    return None

saved = 0
skipped = 0
for q in data:
    qid = q.get("question_id")
    if qid is None:
        print("Skipping entry without question_id")
        skipped += 1
        continue
    answers = fetch_answers_for_q(qid)
    if answers is None:
        skipped += 1
    else:
        try:
            (out / f"{qid}.json").write_text(
                json.dumps({"question": q, "answers": answers}, indent=2), encoding="utf-8"
            )
            print("Saved answers for:", qid)
            saved += 1
        except Exception as e:
            print(f"[{qid}] Error saving file: {e}")
            skipped += 1
    time.sleep(SLEEP_BETWEEN)

print(f"Done. Saved: {saved}, Skipped: {skipped}")
