# Task Manager API

This is a FastAPI-based task manager API built to track team tasks, monitor progress, and generate quarterly reports.

## Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy + PostgreSQL
- Docker + Docker Compose
- Pytest
- Git + GitHub

## Features
- Create, read, update, delete tasks
- Filter tasks by quarter
- Quarterly statistics report (total, completed, completion rate, by priority, by type)
- Automated tests

## Getting Started

### Requirements
- Docker
- Docker Compose

### Run the project
```bash
docker-compose up --build
```

### API Docs
Open http://127.0.0.1:8000/docs

## Running Tests
```bash
pytest tests/ -v
```