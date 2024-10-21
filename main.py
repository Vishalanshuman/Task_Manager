from fastapi import FastAPI
from app.auth import router as auth_router 
from app.tasks import router as tasks_router
from config import Base,engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router)

