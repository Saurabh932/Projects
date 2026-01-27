from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
import uuid

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import verify_password, create_access_token
from .service import UserService
from .schema import UserModel, UserLogin, UserApproval
from .dependencies import RoleCheck, get_current_user

from src.db.db import get_session
from src.db.models import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])
user_service = UserService()
admin_only = RoleCheck(["admin"])


"""
    Sign-up
"""
@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def signup(user_data, session: AsyncSession = Depends(get_session)):
    if await user_service.user_exists(user_data.email, session):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )

    return await user_service.create_user(user_data, session)


"""
    Login
"""
@auth_router.post("/login")
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(user_data.email, session)

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account pending admin approval"
        )

    access_token = create_access_token(
        user_data={
            "email": user.email,
            "user_id": str(user.uid),
            "role": user.role
        },
        expiry=timedelta(hours=1)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "uid": str(user.uid),
            "email": user.email,
            "role": user.role
        }
    }


"""
    Current user
"""
@auth_router.post("/me", response_model=UserModel)
async def me(current_user=Depends(get_current_user)):
    return current_user


"""
    Admin: approve / change role
"""
@auth_router.put(
    "/user/{email}/approve",
    response_model=UserModel,
    dependencies=[Depends(admin_only)]
)
async def approve_user(
    email: str,
    data: UserApproval,
    session: AsyncSession = Depends(get_session)
):
    user = await user_service.get_user_by_email(email, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_service.approve_user(
        user=user,
        is_verified=data.is_verified,
        role=data.role,
        session=session
    )


"""
    Pending users
"""
@auth_router.get("/pending", dependencies=[Depends(admin_only)])
async def get_pending_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.is_verified == False)
    )
    users = result.scalars().all()

    return [{"uid": str(u.uid), "email": u.email} for u in users]


"""
    Reject user
"""
@auth_router.delete("/reject/{uid}", dependencies=[Depends(admin_only)])
async def reject_user(uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, uid)

    if not user:
        raise HTTPException(404, "User not found")

    await session.delete(user)
    await session.commit()

    return {"message": "User rejected and removed"}
