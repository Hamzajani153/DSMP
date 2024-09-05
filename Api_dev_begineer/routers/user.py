# from .. import models , schemas, utils
# from fastapi import FastAPI , Body , Response ,status ,HTTPException , Depends , APIRouter
# from sqlalchemy.orm import Session
# from ..database import get_db

# from .. import models , schemas, utils
import models
import schemas
import utils
from fastapi import FastAPI , Body , Response ,status ,HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
# from ..database import get_db
from database import get_db
from typing import List


router = APIRouter()

@router.post("/users/" ,status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    # hash the password
    
    user.password = utils.hash(user.password) 

    # new_user = models.User(email = user.email, password = user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id:int , db:Session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {user_id} not found")
    return user