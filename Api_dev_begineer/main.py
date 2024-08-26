from typing import Optional
from fastapi import FastAPI , Body , Response ,status ,HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    ratings: int | None = None



new_posts = [{"title": "post1", "content": "content1","id":1},
             {"title": "post2", "content": "content2","id":2}]

def find_post(id):
    for p in new_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(new_posts):
        if p['id'] == id:
            return i
    return None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/")
def create_item():
    return {"hello" : "world"}

@app.post("/add")
def create_postt(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
    


@app.post("/new_post")
def create_post(new_post:Post):
    print(new_post)
    print(new_post.dict())
    print(new_post.model_dump())
    return{"new" :"post_created"}


@app.get("/posts")
def get_posts():
    return {"posts": new_posts}

@app.post("/new_posts", status_code= status.HTTP_201_CREATED)
def create_new_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    new_posts.append(post_dict)
    # print(new_posts)
    return {"data": post_dict}


@app.get("/posts/{post_id}")
def get_post(post_id: int , response: Response):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"post with id {post_id} not found"}
    return {"post": f"here is post {post}"}


@app.delete("/posts/{post_id}")
def post_delete(post_id: int):
    index = find_index_post(post_id)   

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")

    new_posts.pop(index) # type: ignore
    return {"message": "post deleted successfully"}

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index = find_index_post(post_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
    post_dict = post.dict()
    post_dict['id'] = post_id
    new_posts[index] = post_dict
    return {"message": "post updated successfully"}
