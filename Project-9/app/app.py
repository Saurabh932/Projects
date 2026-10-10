from sqlalchemy.sql.coercions import expect
from logging import exception
from h11._abnf import status_code
import os
import uuid
import shutil
import tempfile

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends

from app.schema import PostCreate,  PostResponse, UserRead, UserCreate, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session, User
from app.users import auth_backend, current_active_user, fastapi_users
from app.image import imagekit
from imagekitio import ImageKit

from sqlalchemy import  select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserCreate), prefix="/users", tags=["users"])



@app.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      caption: str = Form(""),
                      user: User = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):

    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        with open(temp_file_path, "rb") as upload_file:
            upload_result = imagekit.files.upload(
                file=upload_file,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"]
            )

        post = Post(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type.startswith("video/") else "image",
            file_name=upload_result.name
        )

        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()



@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": user.id,
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )
    
    return {"posts": posts_data}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalar()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user.id:
            raise HTTPException(status_code=403,  detail="You don't have permission to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =======================================================================================================

# text_posts = {
#     "1":{"title":"First Post", "content":"This is first"},
#     "2":{"title":"Second Post", "content":"This is second"},
#     "3":{"title":"Third Post", "content":"This is third"},
#     "4":{"title":"Fourth Post", "content":"This is fourth"},
#     "5":{"title":"Fifth Post", "content":"This is fifth"},
#     }

# @app.get("/posts")
# def get_all_posts(limit:int = None):
#     # if len(text_posts) == 0:
#     #     raise HTTPException(status_code=404, detail="No posts found")
#     # return text_posts

#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts 

# @app.get("/posts/{post_id}")
# def get_post_by_id(post_id: str):
#     if post_id in text_posts:
#         return text_posts[post_id]
#     raise HTTPException(status_code=404, detail="Post not found")


# @app.post("/posts", response_model=PostResponse, status_code=201)
# def create_post(post: PostCreate) -> PostResponse:
#     new_id = str(int(max(text_posts.keys()))+1)
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[new_id] = new_post
#     return {"status_code": 201, "detail": "Post Created Successfully", "data": new_post}