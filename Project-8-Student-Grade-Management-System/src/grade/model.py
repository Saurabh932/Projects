import uuid
from sqlmodel import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mysql import CHAR

from typing import Optional
from datetime import datetime

class Student(SQLModel, table=True):
    __tablename__="student"
    uid : Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    )
    name : str
    total_marks : int
    total_sub : int
    average : float = 0.0
    grade : str = "F"
    created_at : datetime = Field(default_factory=datetime.now)
    updated_at : Optional[datetime] = Field(default_factory=datetime.now)
    
    
    # def calculate_grade(self):
    #     """Calculates average and grade automatically."""
    #     if self.total_subjects <= 0:
    #         return {"error": "Invalid number of subjects."}

    #     self.average = self.total_marks / self.total_subjects

    #     if self.average >= 90:
    #         self.grade = "A"
    #     elif 75 <= self.average < 90:
    #         self.grade = "B"
    #     elif 45 <= self.average < 75:
    #         self.grade = "C"
    #     else:
    #         self.grade = "F"
