"""Router messages"""
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
from src.app.logic.groups_logic import logic_get_group_by_id, logic_user_in_group
from src.app.utils.websockets import live
from src.database.database import get_session
from src.database.models import User, Group, Message


message_router = APIRouter(prefix="/messages")

@message_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReturnMessage,
    dependencies=[Depends(live)]
)
async def write_message(
    message: WriteMessage,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(logic_user_in_group),
    group: Group = Depends(logic_get_group_by_id)
):
    """Write a message in a group"""
    return await logic_make_message(database, user, group, message.message, message.reply_id)


@message_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ReturnMessages,
    dependencies=[Depends(logic_user_in_group)]
)
async def get_messages_in_group(
    messages: ReturnMessages = Depends(logic_get_messages_by_group)
):
    """Get all messages written in a group"""
    return messages


@message_router.get(
    "/{user_name}",
    status_code=status.HTTP_200_OK,
    response_model=ReturnMessages,
    dependencies=[Depends(logic_user_in_group)]
)
async def get_messages_in_group_by_name(
    messages: ReturnMessages = Depends(logic_get_messages_by_user_in_group)
):
    """Get all messages written in a group"""
    return messages


@message_router.put(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(live)]
)
async def change_message(
    new_message: WriteMessage,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(logic_user_in_group),
    message: Message = Depends(logic_get_message_by_id)
):
    """Change a message"""
    await logic_edit_message(database, message, new_message.message, user)


@message_router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(live)]
)
async def delete_message(
    database: AsyncSession = Depends(get_session),
    user: User = Depends(logic_user_in_group),
    message: Message = Depends(logic_get_message_by_id)
):
    """Change a message"""
    await logic_delete_message(database, message, user)
