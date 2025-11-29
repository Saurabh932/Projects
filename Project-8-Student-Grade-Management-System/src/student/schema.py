import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date

from src.grade.schema import SubjectResponse


class StudentResponseModel(BaseModel):
    uid: uuid.UUID
    name: str
    average: Optional[float] = None
    grade: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


    

class StudentBase(BaseModel):
    name: str
    total_mark: int = Field(ge=0)
    total_marks: int = Field(ge=1)


class StudentCreateModel(BaseModel):
    name: str   
    total_marks : int
    total_sub : int
    

class StudentUpdateModel(BaseModel):
    name: Optional[str] = None
    total_marks: int | None = None
    total_sub: int | None = None