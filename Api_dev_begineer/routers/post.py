# from .. import models , schemas, utils
import models
import schemas
import utils
from fastapi import FastAPI , Body , Response ,status ,HTTPException , Depends , APIRouter 
from sqlalchemy.orm import Session
from fastapi import Depends
# from ..database import get_db
from database import get_db
from typing import List
import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/posts", #we don't need to write /posts in every path we use / instead
    tags=["posts"]
)

@router.post("/add")
def create_postt(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
    


@router.post("/new_post")
def create_post(new_post:schemas.PostCreate):
    print(new_post)
    print(new_post.dict())
    print(new_post.model_dump())
    return{"new" :"post_created"}


# @router.get("/posts")
# def get_posts():
#     curr.execute("  "" SELECT * FROM post""")
#     posts = curr.fetchall()
#     print(posts)
#     return {"posts": posts}

# @router.post("/new_posts", status_code= status.HTTP_201_CREATED)
# def create_new_post(post: schemas.PostCreate):
    
#     # This is work but this can cause a sql injection probelem which attacker is used.
#     # curr.execute(f"""INSERT INTO post (title, content) VALUES ('{post.title}', '{post.content}')""")
#     # so we use
#     curr.execute("""INSERT INTO post (title, content,published) VALUES (%s, %s,%s) 
#                  RETURNING *""",(post.title, post.content,post.published))
#     new_post = curr.fetchone()
#     conn.commit()
#     return {"new_post": new_post}

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_postss(post:schemas.PostCreate , db:Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title = post.title, content = post.content,
    #                         published = post.published)
    print(current_user.id) # type: ignore
    new_post = models.Post(owner_id = current_user.id,**post.model_dump()) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    

# @router.post("/fetch_one/{post_id}")
# def get_onepost(post_id: int):
#     curr.execute(""" SELECT * FROM post where id = %s """,(str(post_id)))
#     post = curr.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {post_id} not found")
#     return {"post": post}
    

@router.get("/{post_id}")
def get_post(post_id: int , db:Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(post_id)
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {post_id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"post with id {post_id} not found"}
    return post


# @router.delete("/posts/{post_id}")
# def post_delete(post_id: int):
#     index = find_index_post(post_id)   

#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {post_id} not found")

#     new_posts.pop(index) # type: ignore
#     return {"message": "post deleted successfully"}

@router.delete("/delete_post/{post_id}", status_code= status.HTTP_204_NO_CONTENT)
def del_post(post_id:int , db:Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
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

# @router.put("/posts/{post_id}")
# def update_post(post_id: int, post: PostCreate):
#     index = find_index_post(post_id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {post_id} not found")
#     post_dict = post.dict()
#     post_dict['id'] = post_id
#     new_posts[index] = post_dict
#     return {"message": "post updated successfully"}

@router.put("/update_post/{post_id}")
def updated_post(post_id:int, post:schemas.PostCreate, db:Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

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
    post_query.update(post.model_dump(), synchronize_session=False) #type: ignore
    db.commit()
    return {"data": post_query.first()}