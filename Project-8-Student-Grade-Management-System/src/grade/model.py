from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Student(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    total_marks : int
    total_sub : int
    average : float = 0
    grade : str = "F"
    created_at : datetime = Field(default_factory=datetime)
    update_at : datetime = Field(default_factory=datetime)
    
    
    def calculate_grade(self):
        """Calculates average and grade automatically."""
        if self.total_subjects <= 0:
            return {"error": "Invalid number of subjects."}

        self.average = self.total_marks / self.total_subjects

        if self.average >= 90:
            self.grade = "A"
        elif 75 <= self.average < 90:
            self.grade = "B"
        elif 45 <= self.average < 75:
            self.grade = "C"
        else:
            self.grade = "F"
