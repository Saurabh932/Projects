from  pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    status_code: int
    detail: str
    data: PostCreate