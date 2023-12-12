"""Code to make a database connection"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# pylint: disable=unused-import
import src.database.models

from src.settings import DB_NAME

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_NAME}.db",
    connect_args={"check_same_thread": False}, echo=True)



async def get_session() -> AsyncGenerator:
    """get session"""
    async_session = sessionmaker( # type: ignore
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
