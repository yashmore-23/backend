# app/routes/roadmap.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.openrouter import get_roadmap_from_openrouter

router = APIRouter()

class GoalInput(BaseModel):
    goal: str

@router.post("/generate-roadmap/")
async def generate_roadmap(goal_input: GoalInput):
    try:
        roadmap = await get_roadmap_from_openrouter(goal_input.goal)
        return {"roadmap": roadmap}
    except ValueError as ve:
        # Catch errors from openrouter.py like quota exceeded or API issues
        return {"error": str(ve)}
    except Exception as e:
        # Other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))

