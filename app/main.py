from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import maskpass
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, pwd, get_db
from .routers import post, user


models.Base.metadata.create_all(bind=engine) # code that creates tables

app = FastAPI()

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


app.include_router(post.router)
app.include_router(user.router)

# decorator turns into a path API using a get 'method' request. "/" is the root 'path'
@app.get("/") 
def root():
    return {"message": "Welcome to my api!!!!!" }





    






## if two paths are the same FastAPI will return the method of the first match

# # POST to postman
# @app.post("/createposts")
# def createpost(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
# # title str, content str



### 6:32:38 on video
### venv\Scripts\activate.bat 
### uvicorn app.main:app --reload 

### need to install psycopg2 to use postgres with sqlalchemy