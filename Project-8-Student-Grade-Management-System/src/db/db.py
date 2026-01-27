from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import config

# creating async database engine using asyncpg
async_engine = create_async_engine(
    config.DATABASE_URL,    # Reading DB url from .env
    echo=True               # displaying SQL queries
)

# Global async sessionmaker
async_session_maker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Function to initialize db and create tables
async def init_db() -> None:
    async with async_engine.begin() as conn:
        # Automatically creates all the tables in models
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Tables created successfully!")

# Dependency: returns an async session (used by FastAPI routes)
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
