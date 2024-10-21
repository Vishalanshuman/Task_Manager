from fastapi import APIRouter,Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from config import get_db
from config.schema import StatusEnum,PriorityEnum,TodoOutput,TodoUpdate,LoginForm,Token,UserCreate,PaginatedTodos,TodoCreate
from config.models import Todo,User
from config.auth import get_current_user,ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/tasks/", response_model=TodoOutput)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        print("user_id--->",current_user.id)
        db_todo = Todo(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            status=todo.status,
            due_date=todo.due_date,
            user_id=current_user.id  
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo  
    except Exception as e:
        return HTTPException(detail=str(e))

@router.get("/tasks/", response_model=PaginatedTodos)
def get_all_todos(
    skip: int = 0,
    limit: int = 10,
    status: Optional[StatusEnum] = None,
    priority: Optional[PriorityEnum] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Todo).filter(Todo.user_id == current_user.id)

    if status:
        query = query.filter(Todo.status == status)
    if priority:
        query = query.filter(Todo.priority == priority)
    if search:
        query = query.filter(
            (Todo.title.ilike(f"%{search}%")) | 
            (Todo.description.ilike(f"%{search}%"))
        )

    sort_mapping = {
        "due_date": Todo.due_date,
        "priority": Todo.priority,
        "created_at": Todo.id 
    }
    if sort_by in sort_mapping:
        query = query.order_by(sort_mapping[sort_by])
    else:
        query = query.order_by(Todo.id)  

    total = query.count()
    todos = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "todos": todos  
    }




@router.get("/tasks/{task_id}", response_model=TodoOutput)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        todo = db.get(Todo, task_id)
        if not todo or todo.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Task Not Found or You don't have access to this task")
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.get(Todo, task_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task Not Found or You don't have access to this task")
    
    db.delete(todo)
    db.commit()
    return {"message": "Task Deleted successfully"}

@router.put("/tasks/{task_id}", response_model=TodoOutput)
def update_task(request: TodoUpdate, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        todo = db.get(Todo, task_id)
        if not todo or todo.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Task Not Found or You don't have access to this task")
        
        todo.title = request.title if request.title else todo.title
        todo.description = request.description if request.description else todo.description
        todo.priority = request.priority if request.priority else todo.priority
        todo.status = request.status if request.status else todo.status
        todo.due_date = request.due_date if request.due_date else todo.due_date
        
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})