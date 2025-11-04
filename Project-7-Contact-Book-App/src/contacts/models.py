"""
This file defines the Contact table structure using SQLModel.
Each class here represents a table in the database.
"""

import uuid
from sqlalchemy import BigInteger
from datetime import datetime
from sqlmodel import SQLModel, Field


class Contact(SQLModel, table=True):
    """
    Contact table structure (DB Model)
    Each instance = one row in the contact details.
    """
    __tablename__ = "contacts"          #Sets actual table name (“contacts”)
    
    # Defining Primary Primary key column using UUID
    uid : uuid.UUID = Field (
     default_factory=uuid.uuid4,        #Automatically generates unique ID
     primary_key=True,
     index=True                     #Adds DB index for faster searching
    )
    
    # Main contact info
    name: str = Field(nullable=False, index=True)       #Makes sure the field can’t be empty
    phone_number : int = Field(nullable=False, index=True)
    email : str = Field(nullable=False, index=True)
    address : str = Field(nullable=False, index=True)
    
    
    # Timestamp columns
    created_at : datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)
    
    # String representation 
    def __repr__(self):
        return f"<Contact {self.name}>"
