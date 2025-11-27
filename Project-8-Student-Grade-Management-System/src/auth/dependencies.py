from typing import Any, List
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import decode_token
from .model import User
from .service import UserService
from src.db.db import get_session


user_service = UserService()

class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)
        token = creds.credentials
        
        token_data = decode_token(token)
        
        if not token_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid or expired token")
            
        return token_data
    
    
async def get_current_user(token_data: dict = Depends(TokenBearer()),
                           session: AsyncSession = Depends(get_session)) -> User:
    email = token_data['user']['email']
    user = await user_service.get_user_by_email(email, session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account not approved by admin yet.")
    
    return user


class RoleCheck:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this action.")
    
    
    