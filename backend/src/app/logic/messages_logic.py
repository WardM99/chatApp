"""The logic of messages"""
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.exceptions.wronguser import WrongUserException
from src.database.crud.message import (
    get_messages_by_group,
    get_messages_by_user_in_group,
    make_message,
    edit_message,
    delete_message,
    get_message_by_id
)
from src.database.models import User, Group, Message


async def logic_get_message_by_id(
        database: AsyncSession,
        message_id: int
) -> Message:
    """Logic to get the message by id"""
    return await get_message_by_id(database, message_id)


async def logic_make_message(
        database: AsyncSession,
        user: User,
        group: Group,
        message: str
) -> Message:
    """Logic to make a message"""
    return await make_message(database, user, group, message)


async def logic_get_messages_by_user_in_group(
        database: AsyncSession,
        user_messages: User,
        group: Group
) -> List[Message]:
    """Logic to get all messages send by a user in a group"""
    return await get_messages_by_user_in_group(database, user_messages, group)


async def logic_get_messages_by_group(
        database: AsyncSession,
        group: Group
) -> List[Message]:
    """Logic to get all messages in a group"""
    return await get_messages_by_group(database, group)


async def logic_edit_message(
        database: AsyncSession,
        message: Message,
        new_message: str,
        user: User
) -> Message:
    """Logic to edit a message"""
    if message.sender_id != user.user_id:
        raise WrongUserException
    return await edit_message(database, message, new_message)


async def logic_delete_message(
        database: AsyncSession,
        message: Message,
        user: User
) -> None:
    """Logic to delete a message"""
    if message.sender_id != user.user_id:
        raise WrongUserException
    await delete_message(database, message)
