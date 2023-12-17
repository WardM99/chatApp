"""Router messages"""
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from src.app.schemas.message import (
    WriteMessage,
    ReturnMessages,
    ReturnMessage
)
from src.app.logic.messages_logic import(
    logic_delete_message,
    logic_edit_message,
    logic_get_messages_by_group,
    logic_get_messages_by_user_in_group,
    logic_make_message,
    logic_get_message_by_id
)
from src.app.logic.users_logic import require_user, get_user_by_name
from src.app.logic.groups_logic import logic_get_group_by_id
from src.database.database import get_session
from src.database.models import User, Group, Message


message_router = APIRouter(prefix="/messages")

@message_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReturnMessage
)
async def write_message(
    group_id: int,
    message: WriteMessage,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """Write a message in a group"""
    group: Group = await logic_get_group_by_id(database, group_id)
    return await logic_make_message(database, user, group, message.message)


@message_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ReturnMessages,
    dependencies=[Depends(require_user)]
)
async def get_messages_in_group(
    group_id: int,
    database: AsyncSession = Depends(get_session)
):
    """Get all messages written in a group"""
    group: Group = await logic_get_group_by_id(database, group_id)
    messages: List[Message] = await logic_get_messages_by_group(database, group)
    return ReturnMessages(messages=messages)


@message_router.get(
    "/{user_name}",
    status_code=status.HTTP_200_OK,
    response_model=ReturnMessages,
    dependencies=[Depends(require_user)]
)
async def get_messages_in_group_by_name(
    group_id: int,
    user_name: str,
    database: AsyncSession = Depends(get_session)
):
    """Get all messages written in a group"""
    group: Group = await logic_get_group_by_id(database, group_id)
    user: User = await get_user_by_name(database, user_name)
    messages: List[Message] = await logic_get_messages_by_user_in_group(database, user, group)
    return ReturnMessages(messages=messages)


@message_router.put(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def change_message(
    message_id: int,
    new_message: WriteMessage,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """Change a message"""
    message: Message = await logic_get_message_by_id(database, message_id)
    await logic_edit_message(database, message, new_message.message, user)


@message_router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_message(
    message_id: int,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """Change a message"""
    message: Message = await logic_get_message_by_id(database, message_id)
    await logic_delete_message(database, message, user)
