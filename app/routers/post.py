from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils, oauth2
from ..database import engine, SessionLocal, pwd, get_db


# Define a new router with prefix and tag
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# GET all posts - Read
@router.get("/", response_model=List[schemas.Post]) 
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # Query the database to get all posts
    posts = db.query(models.Post).all() 

    # Return the posts to the client
    return posts



# Creating a POST - Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createpost(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Create a new post object using the PostCreate schema
    new_post = models.Post(**post.dict())

    print(current_user.email)
    # Add the new post to the database session
    db.add(new_post)

    # Commit the changes to the database
    db.commit()

    # Refresh the new_post object to get the updated id value
    db.refresh(new_post)

    # Return the new post to the client
    return new_post


# GET an individual Post - Read
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query the database to get the post with the specified id
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Raise a 404 exception if the post is not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # Return the post to the client
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query the database to get the post with the specified id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Raise a 404 exception if the post is not found
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")

    # Delete the post from the database
    post_query.delete(synchronize_session=False)

    # Commit the changes to the database
    db.commit()

    # Return a 204 No Content response to the client
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}", response_model=schemas.Post) # send put request to specific ID
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query the database to get the post with the specified id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Raise a 404 exception if the post is not found
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")
    
    # Update the post in the database with the data from the request body
    post_query.update(updated_post.dict(), synchronize_session=False)

    # Commit the changes to the database
    db.commit()

    # Return the updated post to the client
    return post_query.first()
