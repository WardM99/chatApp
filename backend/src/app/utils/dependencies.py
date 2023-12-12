"""Dependencies"""
from typing import AsyncGenerator
import aiohttp


async def get_http_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Get an aiohttp ClientSession to send requests with"""
    async with aiohttp.ClientSession() as session:  # pragma: no cover
        yield session
