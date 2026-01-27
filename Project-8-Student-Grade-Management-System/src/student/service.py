from typing import Optional
from datetime import datetime
import uuid

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Student, User
from .schema import StudentCreateModel, StudentUpdateModel


class StudentService:
    """
        Student profile management (NO auth logic here)
    """

    async def create(
        self,
        student_data: StudentCreateModel,
        session: AsyncSession,
    ) -> Student | dict:
        # Ensure user already exists
        result = await session.execute(
            select(User).where(User.email == student_data.name)
        )
        user = result.scalar_one_or_none()

        if not user:
            return {"error": "User must sign up before student profile is created"}

        # Prevent duplicate student profile
        result = await session.execute(
            select(Student).where(Student.user_uid == user.uid)
        )
        existing = result.scalar_one_or_none()

        if existing:
            return {"error": "Student profile already exists"}

        student = Student(
            uid=uuid.uuid4(),
            name=student_data.name,
            user_uid=user.uid,
            average=None,
            grade=None,
        )

        session.add(student)
        await session.commit()
        await session.refresh(student)

        return student

    async def get_student_by_id(
        self,
        student_uid: uuid.UUID,
        session: AsyncSession,
    ) -> Optional[Student]:
        result = await session.execute(
            select(Student).where(Student.uid == student_uid)
        )
        return result.scalar_one_or_none()

    async def update(
        self,
        student_uid: uuid.UUID,
        student_data: StudentUpdateModel,
        session: AsyncSession,
    ) -> Student | dict:
        student = await self.get_student_by_id(student_uid, session)

        if not student:
            return {"error": "Student not found"}

        if student_data.name:
            student.name = student_data.name

        student.updated_at = datetime.now()

        await session.commit()
        await session.refresh(student)

        return student

    async def delete(
        self,
        student_uid: uuid.UUID,
        session: AsyncSession,
    ) -> dict:
        student = await self.get_student_by_id(student_uid, session)

        if not student:
            return {"error": "Student not found"}

        await session.delete(student)
        await session.commit()

        return {"message": "Student deleted"}
