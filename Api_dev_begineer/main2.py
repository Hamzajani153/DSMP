from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
from models import *
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "ok"}