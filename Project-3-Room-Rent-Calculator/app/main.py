from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .core.app import Rent

# app = APIRouter()

# @app.get("/")
# def home():
#     return "Rent!"

# @app.get("/expense")
# def expense(room_rent : int,
#             food : int,
#             wifi : int,
#             electricity : int):
    
#     payment = Rent(room_rent, food, wifi, electricity)
#     result = payment.equal_contri()
#     return result


app = FastAPI()

templates = Jinja2Templates(directory="app/templates/")
app.mount("/static", StaticFiles(directory="app/static"), name='static')


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/expense", response_class=HTMLResponse)
def expense(
            request:Request,
            room_rent : int = Form(...),
            food : int = Form(...),
            wifi : int = Form(...),
            electricity : int = Form(...),
            no_person : int = Form(...)
            ):
    
    payment = Rent(room_rent, food, wifi, electricity, no_person)
    result = payment.equal_contri()
    
    return templates.TemplateResponse("index.html", {"request":request, 'result':result})