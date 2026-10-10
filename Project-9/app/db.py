from fastapi import Depends
from sqlalchemy import ForeignKey, inspect, text
import uuid
from datetime import datetime
from collections.abc import AsyncGenerator

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="posts")


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def _ensure_posts_user_id_column(conn):
    inspector = inspect(conn)
    if 'posts' not in inspector.get_table_names():
        return

    columns = {column['name'] for column in inspector.get_columns('posts')}
    if 'user_id' not in columns:
        conn.execute(text('ALTER TABLE posts ADD COLUMN user_id VARCHAR'))


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_ensure_posts_user_id_column)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session:AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
    