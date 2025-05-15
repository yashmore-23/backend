from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.utils.auth import get_current_user
from app import models, schemas

print("📦 reminder.py loaded")
router = APIRouter()

@router.post("/", response_model=schemas.ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    rem: schemas.ReminderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Ensure goal belongs to this user
    goal = db.query(models.Goal).filter(
        models.Goal.id == rem.goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    new_reminder = models.Reminder(
        remind_at=rem.remind_at,
        goal_id=rem.goal_id
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return new_reminder

@router.get("/", response_model=List[schemas.ReminderResponse])
def list_reminders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Reminder)
        .join(models.Goal)
        .filter(models.Goal.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted = (
        db.query(models.Reminder)
        .join(models.Goal)
        .filter(
            models.Reminder.id == reminder_id,
            models.Goal.user_id == current_user.id
        )
        .delete()
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db.commit()
    return

@router.get("/test")
def test_reminder():
    return {"msg": "reminder router works"}

