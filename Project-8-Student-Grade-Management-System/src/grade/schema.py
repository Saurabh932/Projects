import uuid
from typing import Optional, List
from pydantic import BaseModel, Field


class SubjectCreation(BaseModel):
    subject_name: str
    marks_obtain: int
    max_marks: int = 100
    teacher_name: Optional[str] = None


class SubjectResponse(BaseModel):
    uid: uuid.UUID
    subject_name: str
    marks_obtain: int
    max_marks: int = 100
    teacher_name: Optional[str] = None

    class Config:
        from_attributes = True


class StudentGradeResponse(BaseModel):
    uid: uuid.UUID
    name: str
    average: Optional[float] = None
    grade: Optional[str] = None
    subjects: List[SubjectResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class SubjectUpdate(BaseModel):
    marks_obtain: Optional[int] = None
    max_marks: Optional[int] = None
    teacher_name: Optional[str] = None
