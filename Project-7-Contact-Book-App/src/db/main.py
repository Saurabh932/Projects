"""
This file manages the database connection to initialize logic.
We use SQLModel + asyncpg for async PostgreSQL operation.
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Creates the actual DB connection engine
from sqlalchemy.orm import sessionmaker     # Factory that generates sessions (DB transactions)
from src.config.config import config 


# Creating an async database engine using asyncpg 
async_engine = create_async_engine(
    config.DATABASE_URL,  # async DB URL from .env
    echo=True,            # Logs SQL queries (useful while developing)
)


# Functions to initalize database and create table
async def init_db() -> None:
    
    async with async_engine.begin() as conn:
        # Automatically create all table defined in models (like Contact), if not exists
        await conn.run_sync(SQLModel.metadata.create_all)
        

# Dependancy: returns an async session (used by FASTAPI routes)
async def get_session() -> AsyncSession:
    sessionLocal = sessionmaker(
        async_engine,
        class_= AsyncSession,
        expire_on_commit=False
    )
    
    async with sessionLocal() as session:
        yield session