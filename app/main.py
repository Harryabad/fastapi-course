from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2 # library for interacting with PostgreSQL databases
from psycopg2.extras import RealDictCursor # library for returning PostgreSQL query results as Python dictionaries
import maskpass # custom library for encrypting and decrypting passwords
import time
from sqlalchemy.orm import Session # library for handling SQLAlchemy sessions
from . import models, schemas, utils # custom modules for models, schemas and utilities
from .database import engine, SessionLocal, pwd, get_db # custom module for setting up database connection and getting a database session
from .routers import post, user, auth # custom modules for routes


# create all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

# instantiate the FastAPI app
app = FastAPI()

# loop until a connection to the PostgreSQL database is established
while True:
    try:
        # connect to the PostgreSQL database with the given parameters and create a cursor to interact with the database
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=pwd, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        # if a connection cannot be established, print an error message and wait for 2 seconds before trying again
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

# Hard-coded as each time program restarts we'd lose the data
# initialize a list of dictionaries that represents blog posts
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite foods", "content": "I like pizza", "id": 2}]

# Function to retrieve a post by id
# define a function that returns a blog post with the given id from the list of posts
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

# define a function that returns the index of a blog post with the given id from the list of posts
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

# include the routes defined in the post.py and user.py modules
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# define a root path for the API
# decorator turns into a path API using a get 'method' request. "/" is the root 'path'
@app.get("/") 
def root():
    return {"message": "Welcome to my api!!!!!" }


# -------------------------------------------

## if two paths are the same FastAPI will return the method of the first match

# # POST to postman
# @app.post("/createposts")
# def createpost(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
# # title str, content str



### 7:50:40 on video
### venv\Scripts\activate.bat 
### uvicorn app.main:app --reload 

### need to install psycopg2 to use postgres with sqlalchemy