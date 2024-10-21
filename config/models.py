from config import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from config.common import StatusEnum,PriorityEnum



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)
    


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.low)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Add user_id
    user = relationship("User", back_populates="todos")  # Relationship

User.todos = relationship("Todo", back_populates="user")
