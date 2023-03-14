from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils
from ..database import engine, SessionLocal, pwd, get_db

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all() #Get all entries from the posts table
#     return {"data": posts}

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# GET all posts - Read
@router.get("/", response_model=List[schemas.Post]) 
def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts """) 
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all() 

    return posts



# Creating a POST - Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createpost(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # # post_dict = post.dict()
    # # post_dict['id'] = randrange(0, 1000000)
    # # my_posts.append(post_dict)

    # ## dont use f string here to avoid sql injection
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ , (post.title, post.content, post.published)) 
    # new_post = cursor.fetchone()  # staging a change and retreives the next set on results

    # conn.commit() ## to save data into database


    #new_post = models.Post(title=post.title, content=post.content, published=post.published) #create new post
    new_post = models.Post(**post.dict()) #unpack dictionary
    db.add(new_post) # add to db
    db.commit() # commit to db
    db.refresh(new_post) # retieve


    return new_post

# # Order Matters! - if get {id} was first would throw an integer error. FIFO
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return post




# GET an individual Post - Read
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) #may need to add a comma after id
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    #print(post)
    return post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # # deleting post - find index in array -> my_posts.pop()
    # #index = find_index_post(id)

    post = db.query(models.Post).filter(models.Post.id == id)


    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")

    post.delete(synchronize_session=False)
    #my_posts.pop(index)
    #return {'message': 'post was successfully deleted'} # will not show as a property of 204 error, shouldn't send data back
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}", response_model=schemas.Post) # send put request to specific ID
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #  (post.title, post.content, post.published, (str(id))))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id) #quick check to find index 

    post_query = db.query(models.Post).filter(models.Post.id == id) #setup query to find post with specific id
    post = post_query.first() # grab specific post

    if post == None: # catch if doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False) # chain update method to the query
    db.commit()

    # post_dict = post.dict() # if it does exists, take front end data and convert to python dictionary
    # post_dict['id'] = id # add the id
    # my_posts[index] = post_dict # for the post within index, replace with new post_dict  update
    return post_query.first()