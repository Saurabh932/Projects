from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.db.db import init_db, async_session_maker
from src.student.routes import router as student_router
from src.auth.routes import auth_router
from src.grade.routes import grade_router

from src.auth.service import UserService
from src.auth.utils import get_hash_password
from src.config.config import config

user_service = UserService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Student Grade Management System...")

    # ⚠️ DEV ONLY: schema creation (Alembic should own schema in prod)
    await init_db()

    # Auto-create Admin if not exists
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

            print(f"👑 Admin auto-created: {config.ADMIN_EMAIL}")

    yield

    print("🛑 Shutting down Student Grade Management System...")


app = FastAPI(
    title="Student Grade Management System",
    version="1.0.0",
    description="FastAPI + SQLModel based project for managing student grades",
    lifespan=lifespan,
)

# ✅ CORS (React-ready, dev-safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(grade_router)

# Frontend (legacy HTML, will be replaced by React)
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)
