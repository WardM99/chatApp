from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import AsyncClient, ASGITransport
from src.database.database import engine

from src.app.app import app
from src.app.utils.dependencies import get_http_session
from src.database.database import get_session
from tests.utils.authorization.auth_client import AuthClient

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


@pytest.fixture
def aiohttp_session() -> AsyncMock:
    """Fixture to get a mock aiohttp.ClientSession instance
    Used to replace the dependency of the TestClient
    """
    yield AsyncMock()


@pytest.fixture
def test_client(database_session: AsyncSession, aiohttp_session: AsyncMock) -> AsyncClient:
    """Fixture to create a testing version of our main application"""

    def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield database_session

    def override_get_http_session() -> Generator[AsyncMock, None, None]:
        """Inner function to override the ClientSession used in the app"""
        yield aiohttp_session

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_http_session] = override_get_http_session
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture
def auth_client(database_session: AsyncSession, aiohttp_session: AsyncMock) -> AuthClient:
    """Fixture to get a TestClient that handles authentication"""

    def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield database_session

    def override_get_http_session() -> Generator[AsyncMock, None, None]:
        """Inner function to override the ClientSession used in the app"""
        yield aiohttp_session

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_http_session] = override_get_http_session
    return AuthClient(database_session, transport=ASGITransport(app=app), base_url="http://test")
