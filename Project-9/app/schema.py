import uuid
from pydantic import BaseModel
from fastapi_users import schemas

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    status_code: int
    detail: str
    data: PostCreate

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass