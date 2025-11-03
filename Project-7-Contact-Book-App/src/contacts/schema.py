"""
This file defines the schemas (Pydantic Model) for request/response validation.
Schemas are used in FastAPI endpoints to control and validate input/output.
"""

import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Base class common use
class ContactBase(BaseModel):
    name : str
    phone_number : int
    email : Optional[EmailStr] = None
    address : Optional[str] = None
    
    
# For creating a new contact
class ContactCreate(ContactBase):
    pass

# For Upedating existing one
class CreateUpdate(ContactBase):
    name : Optional[str] = None
    phone_number : Optional[int] = None
    email : Optional[EmailStr] = None
    address : Optional[str] = None
    
# For reading the contact
class CantactRead(ContactBase):
    uid : uuid.UUID
    created_at : datetime
    updated_at : datetime