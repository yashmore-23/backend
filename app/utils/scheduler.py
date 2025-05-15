# backend/app/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app import models
from app.utils.email import send_email
import logging

scheduler = BackgroundScheduler()
logger = logging.getLogger("reminder-scheduler")

def check_reminders():
    """
    Periodically finds due reminders, sends emails, and marks them as sent.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        due = (
            db.query(models.Reminder)
            .join(models.Reminder.goal)
            .join(models.Goal.owner)
            .filter(models.Reminder.remind_at <= now, models.Reminder.sent == False)
            .all()
        )
        for rem in due:
            goal = rem.goal
            user = goal.owner

            logger.info(f"Reminder due for Goal ID {goal.id} at {rem.remind_at}")

            # Send email
            send_email(
                to_email=user.email,
                subject="⏰ Reminder for your goal",
                body=f"Hi {user.username},\n\nThis is your reminder for the goal: '{goal.title}' scheduled at {rem.remind_at}.\n\nStay focused!\n\n- Goal Tracker"
            )

            # Mark as sent
            rem.sent = True
            db.add(rem)

        db.commit()
    except Exception as e:
        logger.exception("Error checking reminders")
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(check_reminders, "interval", minutes=1, id="check_reminders")
    scheduler.start()
    logger.info("Reminder scheduler started")
    return scheduler

