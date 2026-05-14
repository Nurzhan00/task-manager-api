#src/routers/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Task

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
def get_stats(quarter: str = None, db: Session = Depends(get_db)):
    query = db.query(Task)

    if quarter:
        query = query.filter(Task.quarter_plan == quarter)

    tasks = query.all()
    total = len(tasks)
    completed = len([t for t in tasks if t.status == "Выполнена"])
    in_progress = len([t for t in tasks if t.status == "В работе"])
    cancelled = len([t for t in tasks if t.status == "Отменена"])

    by_priority = {
        "Высокий": len([t for t in tasks if t.priority == "Высокий"]),
        "Средний": len([t for t in tasks if t.priority == "Средний"]),
        "Низкий": len([t for t in tasks if t.priority == "Низкий"]),
    }

    by_type = {}
    for task in tasks:
        if task.task_type:
            by_type[task.task_type] = by_type.get(task.task_type, 0) + 1

    return {
        "quarter": quarter or "all",
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "cancelled": cancelled,
        "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
        "by_priority": by_priority,
        "by_type": by_type,
    }