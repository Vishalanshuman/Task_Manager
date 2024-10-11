from pydantic import BaseModel
from fastapi import FastAPI,requests
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config import get_db,Todo,Base,engine,TodoCreate,TodoOutput,TodoUpdate
from datetime import datetime

app = FastAPI()

Base.metadata.create_all(bind=engine)


class PaginatedTodos(BaseModel):
    total: int
    skip: int
    limit: int
    todos: List[TodoOutput]



# Create a new todo
@app.post("/tasks/")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        status=todo.status,
        due_date=todo.due_date 
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/tasks/", response_model=PaginatedTodos)  
def get_all_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(Todo).count()

    todos = db.query(Todo).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "todos": todos  
    }

@app.get("/tasks/{task_id}",response_model=TodoOutput)
def get_task(task_id:int, db:Session=Depends(get_db)):
    try:
        todo = db.get(Todo,task_id)
        if not todo:
            return HTTPException(status_code=404,detail="Task Not Found")
        return todo

    except Exception as e:
        return HTTPException(status_code=404,detail={"error":e.__str__()}
) 


@app.delete("/tasks/{task_id}")
def get_task(task_id:int, db:Session=Depends(get_db)):
    todo = db.get(Todo,task_id)
    if todo is None:
        return HTTPException(status_code=404,detail="Task Not Found")
    db.delete(todo)
    db.commit()
    return {"message":"Task Deleted successfully"}

@app.put("/tasks/{task_id}",response_model=TodoOutput)
def get_task(request:TodoUpdate,task_id:int, db:Session=Depends(get_db)):
    try:
        todo = db.get(Todo,task_id)
        if todo is None:
            return HTTPException(status_code=404,detail="Task Not Found")
        todo.title = request.title if request.title else todo.title
        todo.description = request.description if request.description   else todo.description
        todo.priority = request.priority if request.priority  else todo.priority
        todo.status = request.status if request.status  else todo.status
        todo.due_date = request.due_date if request.due_date  else todo.due_date
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        return HTTPException(status_code=500,detail={"error":e.__str__()})