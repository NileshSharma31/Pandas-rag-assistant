# backend/app.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from backend.retriever import retrieve
import requests
import os

# load .env if you need other settings; not required for Ollama
load_dotenv()

app = FastAPI()

# Serve the UI (ui/index.html) at /ui
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")


@app.get("/")
def home():
    return {
        "status": "ok",
        "info": "RAG backend running. Use /ui for UI or /docs for Swagger.",
    }


class Query(BaseModel):
    query: str
    top_k: int = 5


def build_prompt(user_query: str, results):
    """
    Ultra-small prompt for low-RAM, low-CPU systems.
    """
    context_parts = []

    for r in results[:2]:  # HARD LIMIT TO 2 CHUNKS
        text = (r.get("text") or "")[:600]  # HARD LIMIT PER CHUNK
        context_parts.append(text)

    context = "\n---\n".join(context_parts)

    prompt = f"""
You are a pandas assistant.
Answer using ONLY the context.
Give:
1) direct answer
2) minimal python code
3) one caution

Question:
{user_query}

Context:
{context}
"""
    return prompt.strip()

def call_llm(prompt: str) -> str:
    """
    Call a local LLM served by Ollama.

    For your 4 GB RAM setup, use a small model like `phi3:mini`.

    Make sure you've run:
        ollama pull tinyllama

    If you pulled some other name, change the "model" field below.
    """
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",  # must match the model name you pulled with ollama
                "prompt": prompt,
                "stream": False,
            },
            timeout=90,
        )
        resp.raise_for_status()
        data = resp.json()
        # Non-streaming /generate returns {"response": "...", ...}
        return (data.get("response") or "").strip()
    except Exception as e:
        return f"[LLM error (Ollama): {e}]"


@app.post("/query")
async def query_api(q: Query):
    # 1) retrieve relevant chunks from FAISS
    results = retrieve(q.query, q.top_k)

    # 2) build prompt from query + retrieved context
    prompt = build_prompt(q.query, results)

    # 3) ask local LLM via Ollama
    answer = call_llm(prompt)

    # 4) fallback: if LLM fails or returns empty, show best retrieved snippet
    if (not answer) or answer.startswith("[LLM error"):
        if results:
            top = results[0]
            fallback_text = top.get("text") or ""
            answer = (
                f"{answer}\n\n"
                "Fallback: most relevant retrieved snippet:\n\n"
                f"Source: {top.get('source')} | URL: {top.get('url')}\n\n"
                f"{fallback_text}"
            )
        else:
            answer = f"{answer}\n\nNo retrieved snippets."

    return {
        "query": q.query,
        "results": results,
        "answer": answer,
    }
