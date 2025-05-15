import requests
from fastapi import HTTPException
from app.config import OPENROUTER__API_KEY  # Assuming you'll add this to your config

# OpenRouter.ai API URL
OPENROUTER_AI_API_URL = "https://openrouter.ai/api/v1"

def get_roadmap_from_openrouter(goal_title: str, goal_description: str) -> dict:
    """
    Make a request to OpenRouter.ai to generate a roadmap for the given goal.

    :param goal_title: The title of the goal
    :param goal_description: A description of the goal
    :return: The generated roadmap as a dictionary
    """
    data = {
        "goal": goal_title,
        "description": goal_description,
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_AI_API_KEY}",
    }

    try:
        response = requests.post(OPENROUTER_AI_API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP error responses
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenRouter.ai: {e}")

