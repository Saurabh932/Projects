import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date

class StudentResponseModel(BaseModel):
    uid : uuid.UUID
    name : str
    total_marks : int
    total_sub : int
    average : float
    grade : str
    created_at : datetime
    updated_at : Optional[datetime] = None
    
    class Config:
        from_attributes = True
    

class StudentBase(BaseModel):
    name: str = Field(max_length=100)
    total_mark: int = Field(ge=0)
    total_marks: int = Field(ge=1)


class StudentCreateModel(BaseModel):
    name: str   
    total_marks : int
    total_sub : int
    

class StudentUpdateModel(BaseModel):
    name: str | None = None
    total_marks: int | None = None
    total_sub: int | None = None