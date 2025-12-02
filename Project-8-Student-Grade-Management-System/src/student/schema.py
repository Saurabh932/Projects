import uuid
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class StudentResponseModel(BaseModel):
    uid: uuid.UUID
    name: str
    average: Optional[float] = None
    grade: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentCreateModel(BaseModel):
    name: str


class StudentUpdateModel(BaseModel):
    name: Optional[str] = None
