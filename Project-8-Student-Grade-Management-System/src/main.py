from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.db import init_db, get_session
from src.student.routes import router
from src.auth.routes import auth_router
from src.grade.routes import grade_router
from src.auth.service import UserService
from src.auth.utils import get_hash_password
from src.config.config import config

user_service = UserService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Student Grade Management System...")
    await init_db()

    # Auto-create Admin if not exists
    async for session in get_session():
        admin = await user_service.get_user_by_email(config.ADMIN_EMAIL, session)
        if admin:
            break

        password_hash = get_hash_password(config.ADMIN_PASSWORD)

        await user_service.create_admin(
            email=config.ADMIN_EMAIL,
            password_hash=password_hash,
            session=session
        )

        print(f"👑 Admin auto-created: {config.ADMIN_EMAIL}")
        break

    yield

    print("🛑 Shutting down Student Grade Management System...")


app = FastAPI(
    title="Student Grade Management System",
    version="1.0.0",
    description="FastAPI + SQLModel based project for managing student grades",
    lifespan=lifespan
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(grade_router)
