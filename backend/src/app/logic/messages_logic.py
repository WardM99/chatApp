"""The logic of messages"""
from typing import List, Optional
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.exceptions.wronguser import WrongUserException
from src.app.logic.groups_logic import logic_get_group_by_id
from src.app.logic.users_logic import logic_get_user_by_name
from src.app.schemas.message import ReturnMessage, ReturnMessages
from src.database.crud.message import (
    get_messages_by_group,
    get_messages_by_user_in_group,
    make_message,
    edit_message,
    delete_message,
    get_message_by_id
)
from src.database.database import get_session
from src.database.models import User, Group, Message


async def logic_get_message_by_id(
        message_id: int,
        database: AsyncSession = Depends(get_session)
) -> Message:
    """Logic to get the message by id"""
    return await get_message_by_id(database, message_id)


async def message_to_return_message(message: Message, database: AsyncSession) -> ReturnMessage:
    """Helper function to change a Message to a ReturnMessage"""
    reply_message: Optional[Message] = None
    if message.reply_id:
        reply_message = await get_message_by_id(database, message.reply_id)
    return ReturnMessage(
        message_id=message.message_id,
        message=message.message,
        sender_id=message.sender_id,
        sender=message.sender,
        group_id=message.group_id,
        group=message.group,
        reply_id=message.reply_id,
        reply=reply_message
    )


async def logic_make_message(
        database: AsyncSession,
        user: User,
        group: Group,
        message: str,
        reply_id: Optional[int] = None
) -> ReturnMessage:
    """Logic to make a message"""
    new_message: Message = await make_message(database, user, group, message, reply_id)
    return await message_to_return_message(new_message, database)


async def logic_get_messages_by_user_in_group(
        database: AsyncSession = Depends(get_session),
        user: User = Depends(logic_get_user_by_name),
        group: Group = Depends(logic_get_group_by_id),
        page: int = 1
) -> ReturnMessages:
    """Logic to get all messages send by a user in a group"""
    messages_by_user_in_group: List[Message] =\
        await get_messages_by_user_in_group(database, user, group, page=page)
    return_messages: List[ReturnMessage] = []
    for m in messages_by_user_in_group:
        return_messages.append(
            await message_to_return_message(m, database)
        )
    return ReturnMessages(messages=return_messages)

async def logic_get_messages_by_group(
        database: AsyncSession = Depends(get_session),
        group: Group = Depends(logic_get_group_by_id),
        page: int = 1
) -> ReturnMessages:
    """Logic to get all messages in a group"""
    messages_in_group: List[Message] = await get_messages_by_group(database, group, page=page)
    return_messages: List[ReturnMessage] = []
    for m in messages_in_group:
        return_messages.append(
            await message_to_return_message(m, database)
        )
    return ReturnMessages(messages=return_messages)


async def logic_edit_message(
        database: AsyncSession,
        message: Message,
        new_message: str,
        user: User
) -> ReturnMessage:
    """Logic to edit a message"""
    if message.sender_id != user.user_id:
        raise WrongUserException
    return await message_to_return_message(
        await edit_message(database, message, new_message), database
    )


async def logic_delete_message(
        database: AsyncSession,
        message: Message,
        user: User
) -> None:
    """Logic to delete a message"""
    if message.sender_id != user.user_id:
        raise WrongUserException
    await delete_message(database, message)
