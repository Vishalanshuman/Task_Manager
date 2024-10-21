from typing import Optional,List
from datetime import datetime
from pydantic import BaseModel,Field,EmailStr
from config.models import User
from config.common import PriorityEnum,StatusEnum


class TodoOutput(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    status: StatusEnum
    due_date: Optional[datetime] = None
    user_id: int  

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    status: StatusEnum
    due_date: Optional[datetime] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[datetime] = None


class PaginatedTodos(BaseModel):
    total: int
    skip: int
    limit: int
    todos: List[TodoOutput] 

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginForm(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)

