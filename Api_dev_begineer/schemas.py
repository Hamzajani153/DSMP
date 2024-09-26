from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None
#     # ratings: int | None = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int 
    created_at: datetime 
    owner_id : int
    owner: UserOut

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None