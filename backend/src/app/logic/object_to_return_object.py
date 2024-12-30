"""Helper file to make a object to a return object"""
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.schemas.group import ReturnGroupBasic
from src.app.schemas.message import ReturnMessageBasic, ReturnMessage
from src.app.schemas.user import ReturnUserBasic, ReturnUser
from src.database.crud.message import get_message_by_id
from src.database.models import User, Group, Message

async def user_to_return_user_basic(user: User) -> ReturnUserBasic:
    """logic to make a ReturnUser from a User"""
    return ReturnUserBasic(
        user_id=user.user_id,
        name=user.name,
        status=user.status
    )

async def user_to_return_user(user: User) -> ReturnUser:
    """logic to make a ReturnUser from a User"""
    user_groups: list[ReturnGroupBasic] = []
    for group in user.groups:
        user_groups.append(await group_to_return_group_basic(group))

    return ReturnUser(
        user_id=user.user_id,
        name=user.name,
        status=user.status,
        groups=user_groups
    )


async def message_to_return_message(message: Message, database: AsyncSession) -> ReturnMessage:
    """Helper function to change a Message to a ReturnMessage"""
    return_reply_message_basic: Optional[ReturnMessageBasic] = None
    if message.reply_id:
        reply_message: Message = await get_message_by_id(database, message.reply_id)
        return_reply_message_basic = await message_to_return_message_basic(reply_message)

    return_user_basic_sender: ReturnUserBasic = await user_to_return_user_basic(message.sender)
    return_group_basic: ReturnGroupBasic = await group_to_return_group_basic(message.group)

    return ReturnMessage(
        message_id=message.message_id,
        message=message.message,
        sender_id=message.sender_id,
        sender=return_user_basic_sender,
        group_id=message.group_id,
        group=return_group_basic,
        reply_id=message.reply_id,
        reply=return_reply_message_basic
    )


async def message_to_return_message_basic(message: Message) -> ReturnMessageBasic:
    """Helper function to change a Message to a ReturnMessageBasic"""
    return_user_basic_sender: ReturnUserBasic = await user_to_return_user_basic(message.sender)
    return ReturnMessageBasic(
        message_id=message.message_id,
        message=message.message,
        sender_id=message.sender_id,
        sender=return_user_basic_sender
    )


async def group_to_return_group_basic(group: Group) -> ReturnGroupBasic:
    """Logic to go from Group to ReturnGroupBaisc"""
    return ReturnGroupBasic(
        group_id=group.group_id,
        name=group.name,
        is_private=group.is_private
    )
