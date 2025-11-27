from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio.session import AsyncSession

from .utils import verify_password, create_access_token
from .service import UserService, UserCreation
from .schema import UserModel, UserLogin, UserApproval
from .dependencies import RoleCheck, get_current_user

from src.db.db import get_session

auth_router = APIRouter(prefix="/auth", tags=['auth'])
user_service = UserService()
admin_only = RoleCheck(['admin'])


"""
    Sign-up endpoints
"""
@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreation, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with {email} already exists.")
        
    new_user = await user_service.create_user(user_data, session)
    
    return new_user



"""
    Login Endpoint
"""
@auth_router.post("/login")
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email, session)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exists.")
    
    user = await user_service.get_user_by_email(email, session)
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password.")
    
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account is pending admin approval.")
    
    access_token = create_access_token(user_data={'email':email, 'user_id':str(user.uid), 'role':user.role},
                                       expiry=timedelta(hours=1))
    
    return {"access_token":access_token, "token_type":"bearer",
            "user":{"uid":str(user.uid),
                    "email":user.email,
                    "role":user.role}}
    
    
"""
    Check the current logged in user.
"""
@auth_router.post("/me", response_model=UserModel)
async def me(current_user = Depends(get_current_user)):
    return current_user


"""
    Admin Only : approve/change roles
"""
@auth_router.put("/user/{email}/approve", response_model=UserModel, dependencies=[Depends(admin_only)])
async def approve_user(email: str, data: UserApproval, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(email, session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user = await user_service.approve_user(user=user, is_verified=data.is_verified,
                                           role=data.role, session=session)
    
    return user