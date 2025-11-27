import uuid
from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.mysql import CHAR
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import UUID


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid : Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, 
                                      primary_key=True, index=True)

    email : str = Field(index=True, unique=True, nullable=False)
    password_hash : str
    
    # "admin" | "student"
    role : str = Field(default="student")
    
    first_name : str | None = None
    last_name : str | None = None   
    
    # Admin approval flag
    is_verified : bool = Field(default=False)
    
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at : Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    
    def __repr__(self):
        return f"<User {self.username}>"