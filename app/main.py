from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import maskpass
import time
from sqlalchemy.orm import Session
from . import models # . = current directory
from .database import engine, SessionLocal, pwd, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# any pydantic model can be converted into a dictionary
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
        password = pwd, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

# Hard-coded as each time program restarts we'd lose the data
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite foods", "content": "I like pizza", "id": 2}]

# Function to retrieve a post by id
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

# decorator turns into a path API using a get 'method' request. "/" is the root 'path'
@app.get("/") 
def root():
    return {"message": "Welcome to my api!!!!!" }

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status: Success"}


# GET all posts - Read
@app.get("/posts") 
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts """) 
    posts = cursor.fetchall()
    return {"data": posts}

# Creating a POST - Create
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    ## dont use f string here to avoid sql injection
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ , (post.title, post.content, post.published)) 
    new_post = cursor.fetchone()  # staging a change and retreives the next set on results

    conn.commit() ## to save data into database

    return {"data": new_post}

# Order Matters! - if get {id} was first would throw an integer error. FIFO
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

# GET an individual Post - Read
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) #may need to add a comma after id
    post = cursor.fetchone()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    #print(post)
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    # deleting post - find index in array -> my_posts.pop()
    #index = find_index_post(id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")
    #my_posts.pop(index)
    #return {'message': 'post was successfully deleted'} # will not show as a property of 204 error, shouldn't send data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}") # send put request to specific ID
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
     (post.title, post.content, post.published, (str(id))))
    
    updated_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id) #quick check to find index 

    if updated_post== None: # catch if doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")

    # post_dict = post.dict() # if it does exists, take front end data and convert to python dictionary
    # post_dict['id'] = id # add the id
    # my_posts[index] = post_dict # for the post within index, replace with new post_dict  update
    return {'data': updated_post}
    



## if two paths are the same FastAPI will return the method of the first match

# # POST to postman
# @app.post("/createposts")
# def createpost(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
# # title str, content str



### 4:31:00 on video
### venv\Scripts\activate.bat 
### uvicorn app.main:app --reload 

### need to install psycopg2 to use postgres with sqlalchemy