# backend/retriever.py
from pathlib import Path
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"

INDEX_PATH = Path("index/faiss_index")
META_PATH = Path("index/ids_metas_texts.pkl")

if not INDEX_PATH.exists():
    raise SystemExit(f"Index file not found: {INDEX_PATH}")
if not META_PATH.exists():
    raise SystemExit(f"Metadata file not found: {META_PATH}")

print("Loading FAISS index...")
index = faiss.read_index(str(INDEX_PATH))

print("Loading metadata...")
with META_PATH.open("rb") as f:
    meta = pickle.load(f)

ids = meta["ids"]
metas = meta["metas"]
texts = meta["texts"]

print("Loading embedding model:", MODEL_NAME)
model = SentenceTransformer(MODEL_NAME)

def retrieve(query: str, top_k: int = 5):
    emb = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(emb)
    D, I = index.search(emb, top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx < 0:
            continue
        results.append({
            "id": ids[idx],
            "score": float(dist),
            "source": metas[idx].get("source"),
            "url": metas[idx].get("url"),
            "text": texts[idx],
        })
    return results

if __name__ == "__main__":
    # quick manual test
    q = "how to merge two dataframes on multiple columns in pandas"
    res = retrieve(q, top_k=3)
    for r in res:
        print("----")
        print("ID:", r["id"])
        print("Score:", r["score"])
        print("Source:", r["source"])
        print("URL:", r["url"])
        print("Text snippet:", r["text"][:300].replace("\n", " "))
