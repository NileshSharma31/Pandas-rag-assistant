# Pandas-rag-assistant
A fully local Retrieval-Augmented Generation (RAG) system for answering Pandas queries using StackOverflow data. It combines FAISS semantic search, SentenceTransformers, and a local LLM via Ollama with a FastAPI backend and interactive chat UI.
Pandas RAG Assistant is a fully local, offline Retrieval-Augmented Generation (RAG) system designed to answer Pandas-related programming questions using real StackOverflow data. The system combines semantic search (FAISS + SentenceTransformers) with a locally hosted Large Language Model (LLM) via Ollama, ensuring zero API cost, no rate limits, and full data privacy.

Users interact with the system through a modern, chat-based web interface. When a query is submitted, the system retrieves the most relevant StackOverflow answers, injects them into a structured prompt, and generates a grounded response using a local LLM. Each response is backed by explicit source citations, making the system suitable for learning, debugging, and academic use.

This project demonstrates a production-grade RAG pipeline, including:

Data ingestion

Vector indexing

Semantic retrieval

Prompt engineering

Local AI inference

API-based backend

Interactive frontend

The system runs efficiently on CPU-only machines with as little as 4 GB RAM, making it ideal for students, offline environments, and low-resource setups.

If you want, I can also provide:

One-line resume bullet

Long academic abstract

Problem statement + objectives

Use-case justification for viva or project defense

Just say which one you need.
