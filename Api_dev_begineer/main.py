from typing import Optional
from fastapi import FastAPI , Body , Response ,status ,HTTPException , Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from models import *
from database import engine , get_db

models.Base.metadata.create_all(bind=engine)

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

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Data": posts}


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
    curr.execute("  "" SELECT * FROM post""")
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

@app.post("/postss", status_code= status.HTTP_201_CREATED)
def create_postss(post:Post , db:Session = Depends(get_db)):
    # new_post = models.Post(title = post.title, content = post.content,
    #                         published = post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"new_post": new_post}
    

@app.post("/fetch_one/{post_id}")
def get_onepost(post_id: int):
    curr.execute(""" SELECT * FROM post where id = %s """,(str(post_id)))
    post = curr.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
    return {"post": post}
    

@app.get("/posts/{post_id}")
def get_post(post_id: int , db:Session = Depends(get_db)):
    # post = find_post(post_id)
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"post with id {post_id} not found"}
    return {"post": post}


@app.delete("/posts/{post_id}")
def post_delete(post_id: int):
    index = find_index_post(post_id)   

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")

    new_posts.pop(index) # type: ignore
    return {"message": "post deleted successfully"}

@app.delete("/delete_post/{post_id}", status_code= status.HTTP_204_NO_CONTENT)
def del_post(post_id:int , db:Session = Depends(get_db)):
#     curr.execute(""" DELETE FROM post where id = %s returning * """,(str(post_id),))
#     delete_post = curr.fetchone()
#     conn.commit()
#     if delete_post == None:
    delete_post = db.query(models.Post).filter(models.Post.id == post_id)
    print(delete_post)
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
    
    delete_post.delete(synchronize_session=False)
    db.commit()
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

@app.put("/update_post/{post_id}")
def updated_post(post_id:int, post:Post, db:Session = Depends(get_db)):

    # curr.execute(""" UPDATE post SET title = %s, content = %s,
    #               published = %s WHERE id=%s RETURNING *""",
    #                 (post.title, post.content, post.published, str(post_id)))
    # update_post = curr.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

