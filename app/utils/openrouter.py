# app/utils/openrouter.py

import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def get_roadmap_from_openrouter(goal: str) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Create a detailed roadmap to achieve the following goal:\n{goal}"

    payload = {
        "model": "openai/gpt-4-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000  # limit tokens to avoid hitting quota limits
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENROUTER_URL, headers=headers, json=payload)

    response.raise_for_status()
    data = response.json()

    logging.info(f"OpenRouter API response data: {data}")

    if "error" in data:
        # Handle OpenRouter error response explicitly
        error_msg = data["error"].get("message", "Unknown error from OpenRouter API.")
        raise ValueError(f"OpenRouter API error: {error_msg}")

    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    else:
        raise ValueError(f"Unexpected API response structure: {data}")

