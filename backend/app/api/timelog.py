from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.timelog import TimeLog
from app.models.user import User
from app.utils.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/timelog", tags=["Time Tracking"])

class TimeLogRequest(BaseModel):
    page_name: str
    duration_seconds: int
    course_id: Optional[int] = None

@router.post("/log")
def log_time(
    data: TimeLogRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.duration_seconds < 5:
        return {"message": "Too short to log"}

    log = TimeLog(
        student_id=current_user.id,
        course_id=data.course_id,
        page_name=data.page_name,
        duration_seconds=data.duration_seconds
    )
    db.add(log)
    db.commit()
    return {"message": "Time logged", "seconds": data.duration_seconds}

@router.get("/summary")
def get_time_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(TimeLog).filter(
        TimeLog.student_id == current_user.id
    ).all()

    total_seconds = sum(l.duration_seconds for l in logs)

    page_times = {}
    for log in logs:
        page = log.page_name
        page_times[page] = page_times.get(page, 0) + log.duration_seconds

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_logs = [
        l for l in logs
        if l.logged_at and l.logged_at.replace(tzinfo=None) >= seven_days_ago
    ]

    daily = {}
    for log in recent_logs:
        day = log.logged_at.strftime("%a") if log.logged_at else "Unknown"
        daily[day] = daily.get(day, 0) + log.duration_seconds

    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily_chart = [
        {"day": d, "minutes": round(daily.get(d, 0) / 60, 1)}
        for d in days_order
    ]

    return {
        "total_seconds": total_seconds,
        "total_minutes": round(total_seconds / 60, 1),
        "total_hours": round(total_seconds / 3600, 2),
        "formatted": format_time(total_seconds),
        "page_breakdown": [
            {"page": k, "minutes": round(v / 60, 1)}
            for k, v in sorted(
                page_times.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ],
        "daily_activity": daily_chart,
        "total_sessions": len(logs),
        "avg_session_minutes": round(
            (total_seconds / len(logs)) / 60, 1
        ) if logs else 0
    }

def format_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"