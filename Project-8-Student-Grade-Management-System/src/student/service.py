from typing import Optional
from datetime import datetime
import uuid
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Student
from .schema import StudentCreateModel, StudentUpdateModel


class StudentService:
    
    '''
        Creating new student and calcuating average and grades.
    '''
    async def create(self, student_data: StudentCreateModel, session: AsyncSession):
        query = select(Student).where(Student.name.ilike(student_data.name))
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            return {"error": "Student already exists"}

        new_student = Student(name=student_data.name)
        session.add(new_student)
        await session.commit()
        await session.refresh(new_student)

        return new_student

    
    
    """
        Fetching/Searching student by name
    """
    async def get_student_by_name(self, name: str, session: AsyncSession) -> Optional[Student]:
        result = await session.execute(select(Student).where(Student.name.ilike(name)))
        return result.scalar_one_or_none()

    
    async def get_student_by_id(self, uid, session):
        result = await session.execute(select(Student).where(Student.uid == uid))
        return result.scalar_one_or_none()
    
    
    async def list_students(self, session: AsyncSession):
        result = await session.execute(select(Student))
        return result.scalars().all()



    """
        Updating the existing student details
    """
    async def update(self, uid, data: StudentUpdateModel, session):
        student = await self.get_student_by_id(uid, session)
        if not student:
            return {"error": "Not found"}

        if data.name:
            student.name = data.name

        session.add(student)
        await session.commit()
        await session.refresh(student)

        return student


    
    """
        Deleting Student details
    """
    async def delete(self, uid, session):
        student = await self.get_student_by_id(uid, session)
        if not student:
            return {"error": "Not found"}

        await session.delete(student)
        await session.commit()
        return {"message": "Deleted"}
    
    

    """
        Viewing all details
    """
    async def view(self, session):
        result = await session.execute(select(Student))
        return result.scalars().all()
