from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.app import WeatherApp

router = APIRouter()
weather = WeatherApp()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html", {'request':request, "weather":[]})


@router.post("/weather", response_class=HTMLResponse)
def weather_temp(request : Request,
                 city : str = Form(...)):
    weather.temperature(city)
    return templates.TemplateResponse("index.html", {'request':request, "weather":weather.view_temperature()})