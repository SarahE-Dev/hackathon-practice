"""Simple Groq API chat app - intentionally includes anti-patterns for practice."""

import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Groq Chat")

# FIX: hardcoded API key (should use env var)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY. Set it in your .env file.")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def call_groq(messages, model: str, temperature: float = 0.7) -> str:
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfigured: missing GROQ_API_KEY")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(GROQ_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Groq request timed out")
    except httpx.HTTPStatusError as e:
        # Avoid dumping secrets; include a small hint only
        raise HTTPException(status_code=502, detail=f"Groq API error: {e.response.status_code}")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Network error contacting Groq")
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid JSON from Groq")

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502, detail="Unexpected response shape from Groq")


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
    # FIX: ANTI-PATTERN: copy-pasted API call logic (duplicated in /summarize)
    reply = await call_groq(
        messages=[{"role": "user", "content": req.message}],
        model=req.model,
    )
    return {"reply": reply, "model": req.model}
 

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    # FIX: ANTI-PATTERN: copy-pasted API call logic (same as /chat)
    prompt = f"Summarize the following text in 2-3 sentences:\n\n{req.text}"
    summary = await call_groq(
        messages=[{"role": "user", "content": prompt}],
        model=req.model,
    )
    return {
        "summary": summary,
        "model": req.model,
        "original_length": len(req.text),
    }
