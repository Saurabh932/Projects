import uuid
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserCreation(BaseModel):
    first_name :  str | None = None
    last_name :  str | None = None
    email : EmailStr
    password : str
    
    
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