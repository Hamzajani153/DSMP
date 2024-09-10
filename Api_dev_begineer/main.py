from typing import Optional
from fastapi import FastAPI , Body , Response ,status ,HTTPException , Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import utils
import models , schemas 
from models import *
from schemas import *
from utils import *
from database import engine , get_db
from routers import post , user , auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",
                                password="Pk135430",cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as e:
        print("Database connection error")
        print(f"Error: {e}")
        time.sleep(5)



new_posts = [{"title": "post1", "content": "content1","id":1},
             {"title": "post2", "content": "content2","id":2}]

def find_post(id):
    for p in new_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(new_posts):
        if p['id'] == id:
            return i
    return None


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item():
    return {"hello" : "world"}

