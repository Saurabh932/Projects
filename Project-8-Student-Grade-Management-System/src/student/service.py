from typing import Optional
from datetime import datetime
import uuid
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Student, User
from src.auth.utils import get_hash_password
from .schema import StudentCreateModel, StudentUpdateModel


class StudentService:
    
    '''
        Creating new student and calcuating average and grades.
    '''
    async def create(self, student_data: StudentCreateModel, session: AsyncSession) -> Student:
        query = select(Student).where(Student.name.ilike(student_data.name))
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            return {"error": "Student with this name already exists."}

        # Create linked USER (student account)
        email = student_data.name.lower().replace(" ", ".") + "@schoolmgmt.com"

        user = User(email=email, password_hash=get_hash_password("test12"), role="student", is_verified=True)

        session.add(user)
        await session.flush()  # ⬅ gives user.uid without commit

        #  Create STUDENT profile linked to user
        student = Student(uid=uuid.uuid4(), name=student_data.name, user_uid=user.uid, average=None, grade=None)

        session.add(student)
        await session.commit()
        await session.refresh(student)

        return student


    
    
    """
        Fetching/Searching student by name
    """
    async def get_student_by_name(self, name: str, session: AsyncSession) -> Optional[Student]:
        result = await session.execute(select(Student).where(Student.name.ilike(name)))
        return result.scalar_one_or_none()


    async def get_student_by_id(self, student_uid: uuid.UUID, session: AsyncSession) -> Optional[Student]:
        result = await session.execute(select(Student).where(Student.uid == student_uid))
        return result.scalar_one_or_none()

    
    async def list_students(self, session: AsyncSession):
        result = await session.execute(select(Student))
        return result.scalars().all()



    """
        Updating the existing student details
    """
    async def update(self, student_uid: uuid.UUID, student_data: StudentUpdateModel, session: AsyncSession) -> Optional[Student]:
        student = await self.get_student_by_id(student_uid, session)
        if not student:
            return {"error": "Student not found"}

        if student_data.name:
            student.name = student_data.name

        student.updated_at = datetime.now()

        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student


    
    """
        Deleting Student details
    """
    async def delete(self, student_uid: uuid.UUID, session: AsyncSession):
        student = await self.get_student_by_id(student_uid, session)
        if not student:
            return {"error": "Student not found"}

        await session.delete(student)
        await session.commit()
        return {"message": f"Student deleted"}
    
    

    """
        Viewing all details
    """
    async def view(self, session: AsyncSession):
        result = await session.execute(select(Student))
        return result.scalars().all()
