from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import config
from src.grade.model import Student

# creating async database engine using asyncpg
async_engine = create_async_engine(
    config.DATABASE_URL,    # Reading DB url from .env
    echo=True       # displaying SQL qureis
)

# Function to initialize db and create table
async def init_db() -> None:
    async with async_engine.begin() as conn:
        # Automatically creates all the tables in models
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Tables created successfully!")

        
        
# # Dependancy: returns an async session (used by FASTAPI routes)
async def get_session() -> AsyncSession:
    sessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with sessionLocal() as session:
        yield session