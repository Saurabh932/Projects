import uuid
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserCreation(BaseModel):
    first_name : str = Field(max_length=20)
    last_name : str = Field(max_length=20)
    email : EmailStr
    password : str = Field(...)
    
    
class UserModel(BaseModel):
    uid: uuid.UUID
    first_name: str
    last_name: str
    
    email: str
    role: str
    is_verified: bool
    
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class UserApproval(BaseModel):
    is_verified: bool
    role: str = Field(default="student")