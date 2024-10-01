from fastapi import FastAPI 
from passlib.context import CryptContext
import models
from models import *
from schemas import *
from utils import *
from database import engine 
from routers import post , user , auth , vote
# from main import app
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

