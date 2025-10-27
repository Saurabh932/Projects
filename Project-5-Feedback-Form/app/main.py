from fastapi import FastAPI, Form, Request
from fastapi.requests import HTTPConnection
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .core.app import FeedbackForm


feed = FeedbackForm()
app = FastAPI()

templates = Jinja2Templates(directory="app/template")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    feed.details.clear()
    return templates.TemplateResponse("index.html", {'request':request, "details":feed.view_form()})


@app.post("/feedback", response_class=HTMLResponse)
def feedback(request:Request,
         user : str = Form(...),
         e_mail : str = Form(...),
         description:str = Form(...)):
    
    feed.username(user)
    feed.contact(e_mail)
    feed.feedback(description)
    return templates.TemplateResponse("index.html", {"request":request, "details":feed.view_form()})