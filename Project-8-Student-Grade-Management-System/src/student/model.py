# import uuid
# from sqlmodel import Column, SQLModel, Field
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.dialects.mysql import CHAR

# from typing import Optional
# from datetime import datetime

# class Student(SQLModel, table=True):
#     # __tablename__="student"
#     uid : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
#     name : str
#     total_marks : int = Field(ge=0)
#     total_sub : int = Field(ge=1)
#     average : float | None = None
#     grade : str | None = Field(default=None, max_length=2)
#     created_at : datetime = Field(default_factory=datetime.now, nullable=False)
#     updated_at : datetime | None = None
    
    
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
