"""Simple Groq API chat app - intentionally includes anti-patterns for practice."""

import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Groq Chat")

# FIX: hardcoded API key (should use env var)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY. Set it in your .env file.")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class ChatRequest(BaseModel):
    message: str
    model: str = "llama-3.3-70b-versatile"


class SummarizeRequest(BaseModel):
    text: str
    model: str = "llama-3.3-70b-versatile"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    # ANTI-PATTERN: copy-pasted API call logic (duplicated in /summarize)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": req.model,
        "messages": [{"role": "user", "content": req.message}],
        "temperature": 0.7,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()
    return {
        "reply": data["choices"][0]["message"]["content"],
        "model": req.model,
    }


@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    # ANTI-PATTERN: copy-pasted API call logic (same as /chat)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    prompt = f"Summarize the following text in 2-3 sentences:\n\n{req.text}"
    payload = {
        "model": req.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()
    # BUG: wrong key - uses 'reply' but should return same structure or
    # crashes when Groq returns an error (no error handling)
    return {
        "summary": data["choices"][0]["message"]["content"],
        "model": req.model,
        "original_length": len(req.text),
    }
