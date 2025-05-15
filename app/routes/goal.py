# backend/app/routes/goal.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.utils.auth import get_current_user
from app import models, schemas
from app.utils.openrouter import get_roadmap_from_openrouter

router = APIRouter()

@router.post("/", response_model=schemas.GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal: schemas.GoalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_goal = models.Goal(
        title=goal.title,
        description=goal.description,
        user_id=current_user.id
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.get("/", response_model=List[schemas.GoalResponse])
def read_goals(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Goal)
        .filter(models.Goal.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.put("/{goal_id}", response_model=schemas.GoalResponse)
def update_goal(
    goal_id: int,
    goal: schemas.GoalUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_goal = (
        db.query(models.Goal)
        .filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id)
        .first()
    )
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    for field, value in goal.dict(exclude_unset=True).items():
        setattr(db_goal, field, value)

    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted = (
        db.query(models.Goal)
        .filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id)
        .delete()
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.commit()
    return

@router.post("/{goal_id}/roadmap", response_model=schemas.RoadmapResponse)
def get_roadmap_for_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Generate a step-by-step roadmap for a specific goal using OpenRouter.ai.
    """
    goal = (
        db.query(models.Goal)
        .filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id)
        .first()
    )

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    try:
        roadmap = get_roadmap_from_openrouter(goal.title, goal.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roadmap generation failed: {str(e)}")

    return {"roadmap": roadmap}

