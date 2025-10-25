from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.app import ToDO

router = APIRouter()
todo = ToDO()

templates = Jinja2Templates(directory="app/templates")

# 🏠 View all tasks
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": todo.view_tasks()})

# ➕ Add new task
@router.post("/add")
def adding_task(task: str = Form(...)):
    todo.add_task(task)
    return RedirectResponse(url="/", status_code=303)

# ✏️ Update task
@router.post("/update")
def updating_task(old_task: str = Form(...), new_task: str = Form(...)):
    todo.update_task(old_task, new_task)
    return RedirectResponse(url="/", status_code=303)

# ❌ Delete task
@router.post("/delete")
def deleting_task(task: str = Form(...)):
    todo.delete_task(task)
    return RedirectResponse(url="/", status_code=303)
