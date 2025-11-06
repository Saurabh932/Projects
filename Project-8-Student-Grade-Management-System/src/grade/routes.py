from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .service import Grade

router = APIRouter()
grade = Grade()
template = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
def home(request:Request):
    return template.TemplateResponse("index.html", {"request":request, "grade":grade.view()})


@router.post("/add", response_class=HTMLResponse)
def create(request:Request,
           name : str = Form(...),
           total_marks : int = Form(...),
           total_sub : int = Form(...)):
    
    creating = grade.create(name, total_marks, total_sub)
    success_msg = f"Student with {name} created!"
    
    return template.TemplateResponse("index.html", {"request":request, "grade":grade.view(), "message":success_msg})


@router.post("/search", response_class=HTMLResponse)
def search(request: Request, name : str = Form(...)):
    found = grade.search(name)
    return template.TemplateResponse("index.html", {"request":request, "search_result":found, "grade":grade.view})


@router.post("/update", response_class=HTMLResponse)
def update(request : Request,
           name : str = Form(...),
           total_marks : int = Form(...), 
           total_sub : int = Form(...)):
    
    updated = grade.update(name, total_marks, total_sub)
    success_msg = f"Grade {name} updated successfully."
    
    return template.TemplateResponse("index.html", {"request":request, "update_grade":updated, "grade":grade.view(), "message":success_msg})


@router.post("/delete", response_class=HTMLResponse)
def delete(request : Request, 
           name : str = Form(...)):
    result = grade.delete(name)
    if isinstance(result, dict) and "error" in result:
        success_msg = result["error"]
    else:
        success_msg = f"Student {name} deleted successfully."
    
    return template.TemplateResponse("index.html", {"request": request, "grade":grade.view(), "message":success_msg})