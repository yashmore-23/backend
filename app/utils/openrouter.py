# app/utils/openrouter.py

import os
import httpx
import logging
from dotenv import load_dotenv
from httpx import HTTPStatusError

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def chat_with_openrouter(messages: list[dict]) -> str:
    """
    Interacts with the OpenRouter AI API using a list of messages for conversational context.
    Each message should be a dictionary with 'role': 'user' or 'assistant' and 'content'.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemma-3n-e4b-it:free",
        "messages": messages,
        "max_tokens": 1000
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    except HTTPStatusError as http_err:
        raise ValueError(f"OpenRouter API HTTP error: {http_err.response.status_code} - {http_err.response.text}")
    except httpx.RequestError as req_err:
        raise ValueError(f"OpenRouter API request error: {str(req_err)}")

    if "error" in data:
        error_msg = data["error"].get("message", "Unknown error from OpenRouter API.")
        raise ValueError(f"OpenRouter API error: {error_msg}")

    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    else:
        raise ValueError(f"Unexpected API response structure: {data}")

async def get_roadmap_from_openrouter(user_prompt: str) -> str:
    """
    Wrapper to generate a roadmap from a user prompt.
    Converts the prompt into the OpenRouter message format and gets the AI response.
    """
    messages = [
        {"role": "user", "content": user_prompt}
    ]
    return await chat_with_openrouter(messages)

