"""CRUD operatations of message"""
from typing import List, Optional

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, col, desc

from src.database.models import User, Message, Group

from src.settings import PAGE_SIZE

async def get_message_by_id(
        database: AsyncSession,
        message_id: int
) -> Message:
    """Get a message by id"""
    statement = select(Message)\
        .where(Message.message_id == message_id)
    results = await database.exec(statement)
    return results.one()


async def get_messages_by_user_in_group(
        database: AsyncSession,
        user: User,
        group: Group
) -> List[Message]:
    """Get all message by a user"""
    statemet = select(Message)\
        .where(Message.sender_id == user.user_id)\
        .where(Message.group_id == group.group_id)\
        .order_by(desc(col(Message.message_id)))
    results = await database.exec(statemet)
    return list(results.all())


async def get_messages_by_group(
        database: AsyncSession,
        group: Group,
        page: int = 1
) -> List[Message]:
    """Get all messages in a group"""
    if page <= 0:
        raise ValueError("Page has to be strict positive")
    statement = select(Message)\
        .where(Message.group_id == group.group_id)\
        .order_by(desc(col(Message.message_id)))\
        .offset((page-1)*PAGE_SIZE)\
        .limit(PAGE_SIZE)
    results = await database.exec(statement)
    return list(results.all())


async def make_message(
    database: AsyncSession,
    sender: User,
    group: Group,
    message: str,
    reply_id: Optional[int] = None
) -> Message:
    """Make a new message"""
    new_message: Message = Message(
        message=message,
        sender_id=sender.user_id,
        group_id=group.group_id,
        reply_id=reply_id
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
