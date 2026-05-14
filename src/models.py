#src/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=True)
    role = Column(String, default="user")  # user, admin
    created_at = Column(DateTime, server_default=func.now())

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="В работе")
    priority = Column(String, default="Средний")
    assignee = Column(String, nullable=True)
    quarter_plan = Column(String, nullable=True)
    quarter_fact = Column(String, nullable=True)
    solution = Column(String, nullable=True)
    task_type = Column(String, nullable=True)
    department = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")