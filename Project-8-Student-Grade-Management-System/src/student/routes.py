from uuid import UUID
from typing import Optional
from fastapi import Query
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .service import StudentService
from src.db.db import get_session, Student
from .schema import StudentResponseModel, StudentCreateModel, StudentUpdateModel

from src.auth.dependencies import TokenBearer, RoleCheck

router = APIRouter(prefix="/students", tags=['students'])
student_service = StudentService()
access_token_bearer = TokenBearer()
admin_only = RoleCheck(["admin"])
read_role = RoleCheck(["admin", "user"])
template = Jinja2Templates(directory="src/templates")


'''
HOME PAGE
'''
# @router.get("/", response_model=list[StudentResponseModel], dependencies=[Depends(read_role)])
# async def home(session : AsyncSession = Depends(get_session), 
#                token_details: dict =  Depends(access_token_bearer)):
#     students = await student_service.view(session)
#     return students


"""
    HOME PAGE and List all students with Search + Pagination + Sort + API + UI Integration
"""
@router.get("/", response_model=list[StudentResponseModel])
async def get_students(search: Optional[str] = Query(None), sort: Optional[str] = Query("name"),
                       order: Optional[str] = Query("asc"), limit: int = Query(10, ge = 1),
                       offset: int = Query(0, ge = 0), session: AsyncSession = Depends(get_session),
                       token_details: dict = Depends(access_token_bearer)):
       
        query = select(Student)
       
        if search:
            query = query.where(Student.name.ilike(f"%{search}%"))
        
        if sort in ["name", "average", "grade"]:
            column = getattr(Student, sort)
            query = query.order_by(column.desc() if order == "desc" else column.asc())

        query = query.limit(limit).offset(offset)

        result = await session.execute(query)
        students = result.scalars().all()

        return students



'''
    Creating / Adding Student
'''
@router.post("/add", status_code=status.HTTP_200_OK, response_model=StudentResponseModel, dependencies= [Depends(admin_only)])
async def create(student_data : StudentCreateModel, session : AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    
    creating = await student_service.create(student_data, session)
    
    if "error" in creating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=creating['error'])

    return creating


'''
    Searching Student
'''
@router.get("/search/{student_uid}", response_model=StudentResponseModel, dependencies=[Depends(read_role)])
async def search(student_uid : UUID, session : AsyncSession = Depends(get_session),
                 token_details: dict = Depends(access_token_bearer)):
    found = await student_service.get_student_by_id(student_uid, session)
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return found



'''
    Updating Student (Admin only)
'''
@router.patch("/update/{student_uid}", response_model=StudentResponseModel)
async def update(student_uid: UUID, student_data: StudentUpdateModel, session: AsyncSession = Depends(get_session), token_detail: dict = Depends(access_token_bearer)):
    
    updated = await student_service.update(student_uid, student_data, session)
    
    if "error" in updated:
        raise HTTPException(status_code=404, detail="Student Not Found")

    return updated


'''
    Deleting Student
'''
@router.delete("/delete/{student_uid}", dependencies=[Depends(admin_only)])
async def delete(student_uid : UUID, session : AsyncSession = Depends(get_session), token_detail: dict = Depends(access_token_bearer)):
    
    result = await student_service.delete(student_uid, session)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return None