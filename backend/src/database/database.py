from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import src.database.models

from settings import DB_NAME

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_NAME}.db",
    connect_args={"check_same_thread": False}, echo=True)

async def get_session():
    with AsyncSession(engine) as session:
        yield session