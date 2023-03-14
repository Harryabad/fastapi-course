from pydantic import BaseModel, EmailStr
from datetime import datetime

# Define a base class for the Post model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Define a Post model for creating new posts
class PostCreate(PostBase):
    pass  # Accept what's in PostBase

# Define a Post model that includes an ID and creation date
class Post(PostBase):
    id: int
    created_at: datetime

    # Configure the model to work with SQLAlchemy
    class Config:
        orm_mode = True

# Define a UserCreate model for creating new users
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Define a UserOut model that omits the user's password
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # Configure the model to work with SQLAlchemy
    class Config:
        orm_mode = True
