from uuid import UUID
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .schema import SubjectCreation, SubjectResponse, StudentGradeResponse, SubjectUpdate
from .service import GradeService

from src.auth.dependencies import RoleCheck, TokenBearer
from src.student.service import StudentService
from src.db.db import get_session
from src.db.models import Student, SubjectMarks, User


grade_router = APIRouter(prefix="/grade", tags=["grade"])
admin_only = RoleCheck(['admin'])
grade_service = GradeService()
student_service = StudentService()
access_token_bearer = TokenBearer()


"""
    Showing students dashboard
"""
@grade_router.get("/me")
async def get_my_grade(session: AsyncSession = Depends(get_session), payload: dict = Depends(access_token_bearer)):

    try:
        user_uid = payload["user"]["user_id"]  # ⭐ FIXED
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid token structure")

    result = await session.execute(
        select(Student).where(Student.user_uid == uuid.UUID(user_uid))
    )
    student = result.scalars().first()

    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    await session.refresh(student, ["subjects"])

    return {
        "name": student.name,
        "average": student.average,
        "grade": student.grade,
        "subjects": student.subjects or []
    }



"""
    Adding subject with there marks (Admin Access Only)
"""
@grade_router.post("/{student_uid}/subject", dependencies=[Depends(admin_only)], response_model=SubjectResponse, status_code=status.HTTP_200_OK)
async def add_subject_marks(student_uid: UUID, subject_data: SubjectCreation, session: AsyncSession = Depends(get_session)):

    student = await student_service.get_student_by_id(student_uid, session)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    subject = await grade_service.add_subject_by_uid(student, subject_data, session)
    return subject



"""
    Getting full details of the student
"""
@grade_router.get("/student/{student_uid}", response_model=StudentGradeResponse)
async def get_student_grade(student_uid: UUID, session: AsyncSession = Depends(get_session)):
    student = await student_service.get_student_by_id(student_uid, session)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = await session.execute(select(SubjectMarks).where(SubjectMarks.student_uid == student.uid))
    subjects = result.scalars().all()

    return StudentGradeResponse(uid=student.uid, name=student.name, average=student.average, grade=student.grade, subjects=subjects)


"""
    Edit Subject Marks (Admin Only)
"""
@grade_router.patch("/subject/{uid}", dependencies=[Depends(admin_only)], response_model=SubjectResponse, status_code = status.HTTP_200_OK)
async def update_subject_marks(uid: UUID, update_data: SubjectUpdate, session:AsyncSession = Depends(get_session)):
    result = await session.execute(select(SubjectMarks).where(SubjectMarks.uid == uid))
    subject = result.scalars().first()

    if not subject:
        raise HTTPException(404, "Subject Not Found")

    if update_data.marks_obtain is not None:
        subject.marks_obtain = update_data.marks_obtain

    if update_data.max_marks is not None:
        subject.max_marks = update_data.max_marks

    if update_data.teacher_name is not None:
        subject.teacher_name = update_data.teacher_name

    session.add(subject)
    await session.commit()

    student = await student_service.get_student_by_id(subject.student_uid, session)
    await grade_service.recalculate(student, session)

    await session.refresh(subject)
    return subject


"""
    Deleting Subject Marks (Admin Only)
"""
@grade_router.delete("/subject/{uid}", dependencies=[Depends(admin_only)])
async def delete_subject(uid: UUID,
                         session: AsyncSession = Depends(get_session)):

    result = await session.execute(select(SubjectMarks).where(SubjectMarks.uid == uid))
    subject = result.scalars().first()

    if not subject:
        raise HTTPException(404, "Subject Not Found")

    student = await student_service.get_student_by_id(subject.student_uid, session)

    await session.delete(subject)
    await session.commit()

    await grade_service.recalculate(student, session)

    return {"message": "Subject deleted successfully"}




