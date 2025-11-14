from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime, date

class StudentRead(BaseModel):
    uid : uuid.UUID
    name : str
    total_marks : int
    total_sub : int
    average : float
    grade : str
    created_at : datetime
    updated_at : Optional[datetime]
    

class StudentCreateModel(BaseModel):
    name: str
    total_marks : int
    total_sub : int
    

class StudentUpdateModel(BaseModel):
    name : str
    total_marks : int
    total_sub : int