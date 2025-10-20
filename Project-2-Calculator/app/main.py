from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Annotated
from .core.app import calculator

app = FastAPI()

# Directing Fastapi to find HTML and CSS file 
templates = Jinja2Templates(directory='app/templates')
app.mount("/static", StaticFiles(directory='app/static'), name='static')

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {'request':request})
    

@app.post("/calculate", response_class=HTMLResponse)
def calculation(
                request: Request,
                input1: int = Form(...),
                input2: int = Form(...),
                operand: str = Form(...)
            ):
    
    result = calculator(input1, input2, operand)
    # return f'result : {result}'
    return templates.TemplateResponse("index.html", {"request": request, "result": result})