from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI Chat"])

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def chat_with_ai(messages: List[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemma-3n-e4b-it:free",  # Free model
        "messages": messages,
        "max_tokens": 1000
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = await chat_with_ai([m.dict() for m in request.messages])
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
