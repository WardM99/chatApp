"""Router messages"""
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status


message_router = APIRouter(prefix="/messages")

@message_router.post("")
async def write_message():
    """Write a message in a group"""
    print("MESSAGE")
