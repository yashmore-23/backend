# app/routes/roadmap.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from app.utils.openrouter import chat_with_openrouter

router = APIRouter()

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatInput(BaseModel):
    messages: List[Message]

@router.post("/chat/")
async def chat_with_ai(chat_input: ChatInput):
    try:
        # Forward the list of messages to OpenRouter
        response = await chat_with_openrouter([message.dict() for message in chat_input.messages])
        return {"response": response}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

