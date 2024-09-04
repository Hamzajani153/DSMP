from pydantic import BaseModel, EmailStr
from datetime import datetime


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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int 
    created_at: datetime 

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int

    class Config:
        orm_mode = True