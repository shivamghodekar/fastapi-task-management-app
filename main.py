from fastapi import FastAPI
from src.utils.db import Base,engine
from src.tasks.models import TaskModel
from src.tasks.router import task_routes
from src.users.router import user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="This is my task management application")

app.include_router(task_routes)
app.include_router(user_routes)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# app.include_router(app)


# fastapi dev main.py