from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from .model import User
from .schema import UserCreation

from .utils import get_hash_password

class UserService:
    """
        Creating user
    """
    async def create_user(self, user_data: UserCreation, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(**user_data_dict)
        new_user.password_hash = get_hash_password(user_data_dict['password'])
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        return new_user
    
    
    """
        Getting email by user
    """
    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    
    """
        Checking if the user exists
    """
    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        
        return True if user is not None else False
    
    
    """
        Permission request to verify the user
    """
    async def approve_user(self, user:User, is_verified: bool, role: str, session: AsyncSession) -> User:
        user.is_verified = is_verified
        user.role = role
        
        await session.commit()
        await session.refresh(user)
        return user