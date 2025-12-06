import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field, Column


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)

    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str
    
    # "admin" | "student"
    role: str = Field(default="student")
    
    first_name: str | None = None
    last_name: str | None = None  
    
    # Admin approval flag
    is_verified: bool = Field(default=False)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # 🟢 NEW: Relationship back to the Student profile
    # uselist=False ensures a one-to-one relationship
    student_profile: Optional["Student"] = Relationship(back_populates="user", sa_relationship_kwargs={
        "uselist": False 
    })
    
    def __repr__(self):
        return f"<User {self.email}>"


class Student(SQLModel, table=True):
    __tablename__ = "student"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    average: float | None = None
    grade: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    # 🟢 NEW: Foreign Key to link to the User account (one-to-one relationship)
    user_uid: uuid.UUID = Field(foreign_key="users.uid", unique=True) 

    # Relationships
    subjects: list["SubjectMarks"] = Relationship(back_populates="student", sa_relationship_kwargs={
        "cascade": "all, delete-orphan"
    })
    
    # 🟢 NEW: Relationship to the User model
    user: User = Relationship(back_populates="student_profile")


class SubjectMarks(SQLModel, table=True):
    __tablename__ = "subjectmarks"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    subject_name: str
    marks_obtain: int
    max_marks: int
    teacher_name: str | None = None
    
    # Foreign Key linking marks to a Student
    student_uid: uuid.UUID = Field(foreign_key="student.uid")

    # Relationship back to the Student
    student: Student | None = Relationship(back_populates="subjects")