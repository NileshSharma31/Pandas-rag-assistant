import requests
from pathlib import Path

OUT = Path("data/docs")
OUT.mkdir(parents=True, exist_ok=True)

pages = [
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html",
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html",
    "https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html",
    "https://pandas.pydata.org/pandas-docs/stable/reference/io.html"
]

for url in pages:
    r = requests.get(url)
    r.raise_for_status()
    name = url.split("/")[-1] or "index"
    (OUT / f"{name}.html").write_text(r.text, encoding="utf-8")
    print("Saved:", name)
