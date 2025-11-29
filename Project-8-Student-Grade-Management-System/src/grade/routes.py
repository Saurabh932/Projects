from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .schema import SubjectCreation, SubjectResponse, StudentGradeResponse
from .service import GradeService

from src.auth.dependencies import RoleCheck
from src.student.service import StudentService
from src.db.db import get_session
from src.db.models import SubjectMarks


grade_router = APIRouter(prefix="/grade", tags=["grade"])
admin_only = RoleCheck(['admin'])
grade_service = GradeService()
student_service = StudentService()


"""
    Adding subject with there marks (Admin Access Only)
"""
@grade_router.post("/{name}/subject", dependencies=[Depends(admin_only)], response_model=SubjectResponse, status_code=status.HTTP_200_OK)
async def add_subject_marks(name: str, subject_data:SubjectCreation, session: AsyncSession = Depends(get_session)):
    try:
        subject = await grade_service.add_subject(name, subject_data, session)
        return subject
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


"""
    Getting full details of the student
"""
@grade_router.get("/{name}", response_model=StudentGradeResponse, status_code=status.HTTP_200_OK)
async def get_student_grade(name: str, session: AsyncSession = Depends(get_session)):
    
    ''' Getting Student First '''
    student = await student_service.get_student_by_name(name, session)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details= "Student Not Found")
    
    ''' Getting all the subjects from the studen '''
    result = await session.execute(select(SubjectMarks).where(SubjectMarks.student_uid==student.uid))
    subjects = result.scalars().all()
    
    ''' Let Pydantic convert ORM objects -> response model(orm_mode=True) '''
    
    return StudentGradeResponse(uid=student.uid,
                                name=student.name,
                                average=student.average,
                                grade=student.grade,
                                subjects=subjects)