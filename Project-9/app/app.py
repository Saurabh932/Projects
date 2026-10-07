from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schema import PostCreate,  PostResponse
from app.db import Post, create_db_and_tables, get_async_session

from sqlalchemy import  select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      caption: str = Form(""),
                      session: AsyncSession = Depends(get_async_session)):
    
    post = Post(caption=caption,
                url="dummy_url",
                file_type="photo",
                file_name="dummy name")

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "created_at": post.created_at.isoformat()
            }
        )
    
    return {"posts": posts_data}


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