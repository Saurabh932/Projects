from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import game_routes
import random

app = FastAPI()

# Tell FastAPI where to find templates (HTML) and static (CSS)
templates = Jinja2Templates(directory='app/templates')
app.mount("/static", StaticFiles(directory='app/static'), name='static')

#   Include routes 
app.include_router(game_routes.router)

'''We are not using pydantic because here we are taking input directly from form and not in json'''    

