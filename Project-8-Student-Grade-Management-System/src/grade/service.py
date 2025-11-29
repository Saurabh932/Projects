import uuid
from typing import Tuple

from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .schema import SubjectCreation
from src.db.models import SubjectMarks

from src.db.models import Student
from src.student.service import StudentService


student_service = StudentService()

class GradeService:
    
    def compute_grade(self, marks_percent):
        if marks_percent >= 90: return "A"
        if marks_percent >= 75: return "B"
        if marks_percent >= 45: return "C"
        return "F"
    
    
    async def add_subject(self, name, data: SubjectCreation, session: AsyncSession):
        student = await student_service.get_student_by_name(name, session)
        if not student:
            raise ValueError("Student Not Found")

        new_sub = SubjectMarks(student_uid=student.uid, **data.model_dump())
        session.add(new_sub)
        await session.commit()

        await self.recalculate(student, session)
        await session.refresh(new_sub)
        return new_sub
    
    
    async def recalculate(self, student, session):
        result = await session.execute(select(SubjectMarks).where(SubjectMarks.student_uid == student.uid))
        subjects = result.scalars().all()

        if not subjects:
            student.average = None
            student.grade = None
        else:
            total_marks = sum(s.marks_obtain for s in subjects)
            total_max = sum(s.max_marks for s in subjects)
            percent = (total_marks / total_max) * 100
            student.average = round(percent, 2)
            student.grade = self.compute_grade(student.average)

        session.add(student)
        await session.commit()
        await session.refresh(student)
