from fastapi import FastAPI
from src.grade.routes import router

app = FastAPI()

app.include_router(router)