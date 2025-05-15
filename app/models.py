from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    goals = relationship("Goal", back_populates="owner")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="goals")

    reminders = relationship("Reminder", back_populates="goal", cascade="all, delete")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    remind_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    sent = Column(Boolean, default=False)

    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    goal = relationship("Goal", back_populates="reminders")
