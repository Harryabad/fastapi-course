# Import necessary FastAPI modules, database models, schemas and utilities
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, SessionLocal, pwd, get_db

# Create an instance of the APIRouter with prefix and tags
router = APIRouter(
    prefix="/users",
    tags=['Users']
) 

# Create a route for creating new user with input validation
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the user's password using the 'hash' function from the 'utils' module
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Create a new user with the input from the user and add to the database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the newly created user
    return new_user

# Create a route for getting user by ID
@router.get('/{id}', response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # Query the database for the user with the given ID
    user = db.query(models.User).filter(models.User.id == id).first()

    # If user not found, raise a HTTP exception with 404 status code and error message
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")
    
    # If user found, return the user
    return user
