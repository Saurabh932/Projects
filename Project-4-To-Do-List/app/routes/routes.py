from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.app import ToDO

router = APIRouter()
todo = ToDO()
tasks = []

templates = Jinja2Templates(directory="app/templates")


"""View all tasks"""
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return  templates.TemplateResponse("index.html", {"request":request, "tasks":todo.view_tasks()})


"""Add new task"""
@router.post("/add", response_class=HTMLResponse)
def adding_task(request: Request,
             task: str = Form(...)):
    todo.add_task(task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": todo.view_tasks()})
 
"""Update task"""   
@router.post("/update", response_class=HTMLResponse)
def updating_task(request: Request, 
                  old_task: str = Form(...), 
                  new_task: str = Form(...)):
    todo.update_task(old_task, new_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": todo.view_tasks()})

"""Delete task"""
@router.post("/delete", response_class=HTMLResponse)
def deleting_task(request: Request,
                  task: str = Form(...)):
    todo.delete_task(task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": todo.view_tasks()})
