from pydantic import BaseModel, EmailStr
from datetime import datetime

# any pydantic model can be converted into a dictionary
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass # accept what's in PostBase

class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime

    # converts sqlalchemy model into a pydantic model (pydantic model only reads if dictionary)
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Do not want to return user their password
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True