from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .core.schema import FeedbackModel
from .core.app import FeedbackForm

app = FastAPI()
feed_obj = FeedbackForm()

templates = Jinja2Templates(directory="app/template")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {'request':request})

@app.post("/api/feedback")
async def feedback(feed: FeedbackModel):
    return {
        "name": feed.name,
        "email": feed.email,
        "description": feed.des
    }
