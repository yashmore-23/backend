# backend/app/main.py

from app.utils.logging_config import setup_logging
# Initialize logging (configured in logging_config.py)
setup_logging()

import logging
from fastapi import FastAPI
from . import models, database
from .routes import user, auth, goal
from app.routes import reminder
from app.utils.scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware

# Create all database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(title="Goal Tracker API")

# Include routers
app.include_router(user.router, tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(goal.router, prefix="/goals", tags=["Goals"])
app.include_router(reminder.router, prefix="/reminders", tags=["Reminders"])

# Start scheduler on startup
@app.on_event("startup")
def on_startup():
    start_scheduler()

# Example route to log some data
@app.get("/")
async def root():
    logger = logging.getLogger("app")
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Goal Tracker"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.0.102:3000",
        ],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

