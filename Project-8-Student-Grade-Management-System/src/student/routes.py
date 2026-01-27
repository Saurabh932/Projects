from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .service import StudentService
from .schema import (
    StudentResponseModel,
    StudentCreateModel,
    StudentUpdateModel,
)

from src.auth.dependencies import RoleCheck, get_current_user
from src.db.db import get_session
from src.db.models import Student, User

router = APIRouter(prefix="/students", tags=["students"])

student_service = StudentService()
admin_only = RoleCheck(["admin"])


"""
    Admin: List students (search + pagination + sorting)
"""
@router.get("/", response_model=list[StudentResponseModel], dependencies=[Depends(admin_only)])
async def get_students(
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("name"),
    order: Optional[str] = Query("asc"),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    query = select(Student)

    if search:
        query = query.where(Student.name.ilike(f"%{search}%"))

    if sort in ["name", "average", "grade"]:
        column = getattr(Student, sort)
        query = query.order_by(column.desc() if order == "desc" else column.asc())

    query = query.limit(limit).offset(offset)

    result = await session.execute(query)
    return result.scalars().all()


"""
    Admin: Create student profile (USER MUST ALREADY EXIST)
"""
@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentResponseModel,
    dependencies=[Depends(admin_only)],
)
async def create_student(
    student_data: StudentCreateModel,
    session: AsyncSession = Depends(get_session),
):
    student = await student_service.create(student_data, session)

    if isinstance(student, dict):
        raise HTTPException(status_code=400, detail=student["error"])

    return student


"""
    Admin: Get student by UID
"""
@router.get(
    "/{student_uid}",
    response_model=StudentResponseModel,
    dependencies=[Depends(admin_only)],
)
async def get_student(
    student_uid: UUID,
    session: AsyncSession = Depends(get_session),
):
    student = await student_service.get_student_by_id(student_uid, session)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


"""
    Admin: Update student
"""
@router.patch(
    "/update/{student_uid}",
    response_model=StudentResponseModel,
    dependencies=[Depends(admin_only)],
)
async def update_student(
    student_uid: UUID,
    student_data: StudentUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated = await student_service.update(student_uid, student_data, session)

    if isinstance(updated, dict):
        raise HTTPException(status_code=404, detail=updated["error"])

    return updated


"""
    Admin: Delete student
"""
@router.delete(
    "/delete/{student_uid}",
    dependencies=[Depends(admin_only)],
)
async def delete_student(
    student_uid: UUID,
    session: AsyncSession = Depends(get_session),
):
    result = await student_service.delete(student_uid, session)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return {"message": "Student deleted"}
