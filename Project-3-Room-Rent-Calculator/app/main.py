from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .core.app import Rent
from .core.schema import RentModel

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

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name='static')


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.post("/api/expense")
async def expense(rent : RentModel):
    
    payment = Rent(rent.room_rent, rent.food, rent.wifi, rent.electricity, rent.no_person)
    result = payment.equal_contri()
    
    return JSONResponse(content={"result":result})