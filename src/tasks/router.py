from fastapi import APIRouter, Depends, status, FastAPI
from src.tasks import contoller
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticate
from src.users.models import UserModel

task_routes = APIRouter(prefix="/tasks")

# app = FastAPI()
# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}



# post endpoint
@task_routes.post("/create", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticate)):
    print(user.id)
    return contoller.create_task(body, db, user)

# get endpoint
@task_routes.get("/all_tasks", response_model=List[TaskResponseSchema], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticate)):
    return contoller.get_tasks(db, user)

# get specific data endpoint

@task_routes.get("/one_task/{task_id}", status_code=status.HTTP_200_OK)
def get_one_task(task_id:int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticate)):
    return contoller.get_one_task(task_id, db)


# put endpoint
@task_routes.put("/update_task/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(body:TaskSchema, task_id:int, db: Session=Depends(get_db), user: UserModel = Depends(is_authenticate)):
    return contoller.update_task(body, task_id, db, user)


# delete endpoint
@task_routes.delete("/delete_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int, db: Session=Depends(get_db), user: UserModel = Depends(is_authenticate)):
    return contoller.delete_task(task_id, db, user)






