from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = {
    "1": {
        "title": "Best pizza in the world",
        "content": "Number one pizza in the world is the authentic Italian pizza from New York.",
        "id": "1"
    },
    "2": {
        "title": "Best pasta in the world",
        "content": "Numbre uno in the world is the authentic Italian pasta from Chicago.",
        "id": "2"
    },
}

@app.get("/")
async def root():
    return {"message": "Hello world! Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": [*my_posts.values()]}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = str(uuid4())[:8]
    my_posts[post_dict['id']] = post_dict
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: str):
    if id not in my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} not found.")
    return {"post_detail": my_posts[id]}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    if id in my_posts:
        my_posts.pop(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    if id in my_posts:
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[id] = post_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} not found.")
    return {"post_detail": my_posts[id]}