from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db.db import init_db
from .grade.routes import router


# Definig lifespan (startup + shutdown event)
@asynccontextmanager
async def lifespan(app : FastAPI):
    print("🚀 Starting Student Grade Management System...")
    await init_db()     # It creates table if they don't exists
    yield
    print("🛑 Shutting down Student Grade Management System...")


app = FastAPI(
    title="Student Grade Management System",
    version="1.0.0",
    description="FastAPI + SQLModel based project for managing student grades",
    lifespan=lifespan
)

app.include_router(router)