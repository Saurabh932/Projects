import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field


class Student(SQLModel, table=True):
    __tablename__ = "student"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    average: float | None = None
    grade: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    subjects: list["SubjectMarks"] = Relationship(back_populates="student", sa_relationship_kwargs={
        "cascade": "all, delete-orphan"
    })


class SubjectMarks(SQLModel, table=True):
    __tablename__ = "subjectmarks"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    subject_name: str
    marks_obtain: int
    max_marks: int
    teacher_name: str | None = None
    student_uid: uuid.UUID = Field(foreign_key="student.uid")

    student: Student | None = Relationship(back_populates="subjects")
