from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# any pydantic model can be converted into a dictionary
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

# GET all posts - Read
@app.get("/posts") 
def get_posts():
    return {"data": my_posts}

# Creating a POST - Create
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    #print(post)
    #print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# Order Matters! - if get {id} was first would throw an integer error. FIFO
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

# GET an individual Post - Read
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    #print(post)
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post - find index in array -> my_posts.pop()
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")
    my_posts.pop(index)
    #return {'message': 'post was successfully deleted'} # will not show as a property of 204 error, shouldn't send data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}") # send put request to specific ID
def update_post(id: int, post: Post):

    index = find_index_post(id) #quick check to find index 

    if index == None: # catch if doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")

    post_dict = post.dict() # if it does exists, take front end data and convert to python dictionary
    post_dict['id'] = id # add the id
    my_posts[index] = post_dict # for the post within index, replace with new post_dict  update

    return {'data': post_dict}
    



## if two paths are the same FastAPI will return the method of the first match

# # POST to postman
# @app.post("/createposts")
# def createpost(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
# # title str, content str



### 1:47:58 on video