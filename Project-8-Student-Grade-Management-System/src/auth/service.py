from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User, Student
from .schema import UserCreation
from .utils import get_hash_password


class UserService:
    async def create_user(self, user_data: UserCreation, session: AsyncSession) -> User:
        data = user_data.model_dump()
        password = data.pop("password")

        user = User(**data)
        user.password_hash = get_hash_password(password)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        return await self.get_user_by_email(email, session) is not None

    async def approve_user(
        self,
        user: User,
        is_verified: bool,
        role: str,
        session: AsyncSession
    ) -> User:
        user.is_verified = is_verified
        user.role = role

        # Check student via correct FK
        result = await session.execute(
            select(Student).where(Student.user_uid == user.uid)
        )
        student = result.scalar_one_or_none()

        if not student:
            student = Student(
                name=f"{user.first_name or ''} {user.last_name or ''}".strip() or "Unnamed Student",
                user_uid=user.uid
            )
            session.add(student)

        await session.commit()
        await session.refresh(user)

        return user
