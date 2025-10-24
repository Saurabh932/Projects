from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import routes

app = FastAPI()

app.mount('/static', StaticFiles(directory="app/static"), name='static')
app.include_router(routes.router)