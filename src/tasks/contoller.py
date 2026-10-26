from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.users.models import UserModel


# post endpoint
def create_task(body:TaskSchema, db:Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title = data["title"], 
                         description = data["description"], 
                         is_completed = data["is_completed"],
                         user_id = user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)


    return new_task

# get endpoint
def get_tasks(db:Session, user: UserModel):
    tasks=db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks


# get endpoint
def get_one_task( task_id:int, db:Session):
    one_task = db.query(TaskModel).get(task_id)

    if not one_task:
        raise HTTPException(status_code=404, detail="Task id is incorrect") # 404 not found error

    return {"status":"Task fetch successfully", "data":one_task}

# put endpoint
def update_task(body:TaskSchema, task_id:int, db:Session, user: UserModel):

    one_task: TaskModel = db.query(TaskModel).get(task_id)
    if not one_task:
            raise HTTPException(status_code=404, detail="Task id is incorrect")

    if one_task.user_id != user.id:
         raise HTTPException(status_code=404, detail="You are not allowed to update this task")

    # one_task.title=body.title
    # one_task.description=body.description
    # one_task.is_completed=body.is_completed # for add all the field present in the table then its update else throwing error

    body=body.model_dump()
    for field, value in body.items():
         setattr(one_task, field, value)
    
    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return {"status":"task updated successfully", "data":one_task}

# delete endpoint
def delete_task(task_id:int, db:Session, user: UserModel):

    one_task: TaskModel = db.query(TaskModel).get(task_id)
    if not one_task:
            raise HTTPException(status_code=404, detail="Task id is incorrect")

    if one_task.user_id != user.id:
         raise HTTPException(status_code=404, detail="You are not allowed to delete this task")

    db.delete(one_task)
    db.commit()

    return None
     





















