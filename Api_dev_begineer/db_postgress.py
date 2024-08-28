from typing import Optional
from fastapi import FastAPI , Body , Response ,status ,HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # ratings: int | None = None

while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",
                                password="Pk135430",cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as e:
        print("Database connection error")
        print(f"Error: {e}")
        time.sleep(5)



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
    curr.execute(""" SELECT * FROM post""")
    posts = curr.fetchall()
    print(posts)
    return {"posts": posts}

@app.post("/new_posts", status_code= status.HTTP_201_CREATED)
def create_new_post(post: Post):
    
    # This is work but this can cause a sql injection probelem which attacker is used.
    # curr.execute(f"""INSERT INTO post (title, content) VALUES ('{post.title}', '{post.content}')""")
    # so we use
    curr.execute("""INSERT INTO post (title, content,published) VALUES (%s, %s,%s) 
                 RETURNING *""",(post.title, post.content,post.published))
    new_post = curr.fetchone()
    conn.commit()
    return {"new_post": new_post}
    

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
