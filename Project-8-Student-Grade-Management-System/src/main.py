from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.db.db import init_db, async_session_maker
from src.student.routes import router as student_router
from src.auth.routes import auth_router
from src.grade.routes import grade_router
from src.ai.routes import ai_router # AI Router included

from src.auth.service import UserService
from src.auth.utils import get_hash_password
from src.config.config import config

import os

user_service = UserService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Student Grade Management System...")
    
    # 1. Initialize Database Tables
    await init_db()

    # 2. Seed Admin User if not exists
    async with async_session_maker() as session:
        admin = await user_service.get_user_by_email(
            config.ADMIN_EMAIL, session
        )

        if not admin:
            password_hash = get_hash_password(config.ADMIN_PASSWORD)
            await user_service.create_admin(
                email=config.ADMIN_EMAIL,
                password_hash=password_hash,
                session=session,
            )
            print(f"✅ Admin auto-created: {config.ADMIN_EMAIL}")

    yield
    print("🛑 Shutting down system...")

app = FastAPI(
    title="Student Grade Management System",
    version="1.0.0",
    description="FastAPI + SQLModel based project for managing student grades",
    lifespan=lifespan,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routes ---
# Ensure these are registered BEFORE the static files
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(grade_router)
app.include_router(ai_router)

# --- Static Files & Frontend ---
FRONTEND_DIR = "frontend"

@app.get("/")
async def serve_root():
    """Serves the main landing page."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend index.html not found"}

# Mounting the static directory last ensures that /api routes take priority
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")