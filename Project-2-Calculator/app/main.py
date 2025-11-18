from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Annotated
from .core.app import calculator
from .core.schema import Calculation

app = FastAPI()

# Directing Fastapi to find HTML and CSS file 
templates = Jinja2Templates(directory='app/templates')
app.mount("/static", StaticFiles(directory='app/static'), name='static')

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {'request':request})
    

@app.post("/api/calculate")
async def calculation(data : Calculation):
    
    result = calculator(data.input1, data.input2, data.operator)
    # return f'result : {result}'
    return JSONResponse(content={"result":result})