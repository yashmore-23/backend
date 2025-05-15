from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(GoalBase):
    completed: Optional[bool] = None

class GoalResponse(GoalBase):
    id: int
    completed: bool
    user_id: int

    class Config:
        from_attributes = True

class ReminderBase(BaseModel):
    remind_at: datetime

class ReminderCreate(ReminderBase):
    goal_id: int

class ReminderResponse(ReminderBase):
    id: int
    sent: bool
    goal_id: int

    class Config:
        from_attributes = True

class RoadmapStep(BaseModel):
    task: str
    due_date: str
    status: str

class RoadmapResponse(BaseModel):
    roadmap: str
