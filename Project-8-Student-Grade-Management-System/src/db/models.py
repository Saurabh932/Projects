import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field


class Student(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(nullable=False, unique=True)

    # Only auto-calculated fields
    average: Optional[float] = None
    grade: Optional[str] = None

    subjects: List["SubjectMarks"] = Relationship(back_populates="student")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = None


class SubjectMarks(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    student_uid: uuid.UUID = Field(foreign_key="student.uid", nullable=False, index=True)
    student: "Student" = Relationship(back_populates="subjects")

    subject_name: str = Field(nullable=False)
    marks_obtain: int = Field(nullable=False)
    max_marks: int = Field(nullable=False, default=100)
    teacher_name: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
