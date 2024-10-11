from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Enum, DateTime
import enum
from typing import Optional,List
from datetime import datetime
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PriorityEnum(str, enum.Enum):
    low = "low"
    high = "high"

class StatusEnum(str, enum.Enum):
    inprogress = "inprogress"
    completed = "completed"
    pending = "pending"




class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)  # Nullable for optional field
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.low)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    due_date = Column(DateTime, nullable=True)  # Now a DateTime field


'''-----------------------pydentic Models ------------------'''

class TodoOutput(BaseModel):
    id:int
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    status: StatusEnum
    due_date: Optional[datetime] = None 

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    status: StatusEnum
    due_date: Optional[datetime] = None 

class TodoUpdate(BaseModel):
    title: str = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[datetime] = None