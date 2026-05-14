#src/main.py
from fastapi import FastAPI
from database import Base, engine
from routers import tasks, stats

app = FastAPI(title="Task Manager API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(tasks.router)
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}