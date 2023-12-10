from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.pool import StaticPool

from src.database.database import engine

import src.database.models

@pytest.fixture(scope="session")  
async def tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture
async def database_session(tables) -> AsyncGenerator[AsyncSession, None]:
    connection = await engine.connect()
    transaction = await connection.begin()
    # AsyncSession needs expire_on_commit to be False
    session = AsyncSession(bind=connection, expire_on_commit=False)
    yield session

    # Clean up connections & rollback transactions
    await session.close()

    # Transactions can be invalidated when an exception is raised
    # which causes warnings when running the tests
    # Check if a transaction is still valid before rolling back
    if transaction.is_valid:
        await transaction.rollback()

    await connection.close()