from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.database.models import User, Message, Group

async def get_messages_by_user_in_group(database: AsyncSession, user: User, group: Group) -> List[Message]:
    """Get all message by a user"""
    statemet = select(Message)\
        .where(Message.sender_id == user.user_id)\
        .where(Message.group_id == group.group_id)
    results = await database.exec(statemet)
    return list(results.all())


async def get_messages_by_group(database: AsyncSession, group: Group) -> List[Message]:
    """Get all messages in a group"""
    statement = select(Message).where(Message.group_id == group.group_id)
    results = await database.exec(statement)
    return list(results.all())


async def make_message(database: AsyncSession, sender: User, group: Group, message: str) -> Message:
    """Make a new message"""
    new_message: Message = Message(
        message=message,
        sender_id=sender.user_id,
        group_id=group.group_id
    )
    database.add(new_message)
    await database.commit()
    return new_message


async def edit_message(database: AsyncSession, message: Message, new_message: str) -> Message:
    """Edit the message"""
    message.message = new_message
    database.add(message)
    await database.commit()
    return message


async def delete_message(database: AsyncSession, message: Message) -> None:
    """Delete a message"""
    await database.delete(message)
    await database.commit()
