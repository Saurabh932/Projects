from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .service import Grade
from src.db.db import get_session
from .schema import StudentRead, StudentCreateModel, StudentUpdateModel


router = APIRouter()
grade = Grade()
template = Jinja2Templates(directory="src/templates")


'''
    HOME PAGE
'''
@router.get("/", response_model=list[StudentRead])
async def home(session : AsyncSession = Depends(get_session)):
    students = await grade.view(session)
    return students


'''
    Creating / Adding Student
'''
@router.post("/add", status_code=status.HTTP_200_OK, response_model=StudentRead)
async def create(request:Request, student_data : StudentCreateModel, session : AsyncSession = Depends(get_session)):
    
    creating = await grade.create(student_data, session)
    
    if "error" in creating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=creating['error'])

    return creating


'''
    Searching Student
'''
@router.post("/search/{name}", response_model=StudentRead)
async def search(name : str, session : AsyncSession = Depends(get_session)):
    found = await grade.get_student_by_name(name, session)
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return found


'''
    Updating Student
'''
@router.post("/update/{name}", response_model=StudentRead)
async def update(name: str, student_data: StudentUpdateModel, session: AsyncSession = Depends(get_session)):
    
    updated = await grade.update(name, student_data, session)
    
    if "error" in updated:
        raise HTTPException(status_code=404, detail=updated["error"])

    return updated


'''
    Deleting Student
'''
@router.post("/delete/{name}", response_model=StudentRead)
async def delete(name : str, session : AsyncSession = Depends(get_session)):
    
    result = await grade.delete(name, session)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return None