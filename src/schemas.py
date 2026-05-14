#src/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    department: Optional[str] = None
    role: str = "user"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department: Optional[str]
    role: str
    created_at: datetime


class TaskCreate(BaseModel):
    sender: str
    subject: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: str = "Средний"
    assignee: Optional[str] = None
    quarter_plan: Optional[str] = None
    department: Optional[str] = None
    task_type: Optional[str] = None
    owner_id: int


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    solution: Optional[str] = None
    completed_at: Optional[datetime] = None
    quarter_fact: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender: str
    subject: str
    description: Optional[str]
    status: str
    priority: str
    assignee: Optional[str]
    quarter_plan: Optional[str]
    quarter_fact: Optional[str]
    solution: Optional[str]
    task_type: Optional[str]
    created_at: datetime
    deadline: Optional[datetime]
    completed_at: Optional[datetime]
    owner_id: int