#tests/test_tasks.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_create_task():
    response = client.post("/tasks/", json={
        "sender": "Test User",
        "subject": "Test Task",
        "description": "Test description",
        "priority": "Высокий",
        "assignee": "Nurzhan",
        "quarter_plan": "Q2 2026",
        "department": "IT",
        "task_type": "Тест",
        "owner_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Test Task"
    assert data["status"] == "В работе"


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404