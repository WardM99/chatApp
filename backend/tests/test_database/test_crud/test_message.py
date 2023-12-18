from typing import List
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound
from src.database.crud.message import(
    get_messages_by_group,
    get_messages_by_user_in_group,
    make_message,
    edit_message,
    delete_message,
    get_message_by_id
)
from src.database.crud.user import make_user
from src.database.crud.group import make_group
from src.database.models import User, Message, Group

async def test_make_message(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    new_message: Message = await make_message(database_session, user, group, "First")
    assert new_message.message == "First"
    assert new_message.group_id == group.group_id
    assert new_message.sender_id == user.user_id
    assert new_message.reply_id is None


async def test_make_reply(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    first_message: Message = await make_message(database_session, user, group, "First")
    second_message: Message = await make_message(database_session, user, group, "Second", first_message.message_id)
    assert second_message.message == "Second"
    assert second_message.group_id == group.group_id
    assert second_message.sender_id == user.user_id
    assert second_message.reply_id == first_message.message_id


async def test_get_message_by_id(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    new_message: Message = await make_message(database_session, user, group, "First")
    message: Message = await get_message_by_id(database_session, new_message.message_id)
    assert new_message == message


async def test_get_message_by_id_dont_exist(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    new_message: Message = await make_message(database_session, user, group, "First")
    with pytest.raises(NoResultFound):
        await get_message_by_id(database_session, new_message.message_id+1)


async def test_get_messages_by_user_in_group(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    user2: User = await make_user(database_session, "User2", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    group2: Group = await make_group(database_session, user1, "Group2")
    message1: Message = await make_message(database_session, user1, group1, "First")
    message2: Message = await make_message(database_session, user1, group1, "Second")
    message3: Message = await make_message(database_session, user2, group1, "3th")
    message4: Message = await make_message(database_session, user1, group2, "4th")

    messages: List[Message] = await get_messages_by_user_in_group(database_session, user1, group1)
    assert len(messages) == 2
    assert message1 in messages
    assert message2 in messages
    assert message3 not in messages
    assert message4 not in messages


async def test_get_messages_by_group(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    user2: User = await make_user(database_session, "User2", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    group2: Group = await make_group(database_session, user1, "Group2")
    message1: Message = await make_message(database_session, user1, group1, "First")
    message2: Message = await make_message(database_session, user1, group1, "Second")
    message3: Message = await make_message(database_session, user2, group1, "3th")
    message4: Message = await make_message(database_session, user1, group2, "4th")

    messages: List[Message] = await get_messages_by_group(database_session, group1)
    assert len(messages) == 3
    assert message1 in messages
    assert message2 in messages
    assert message3 in messages
    assert message4 not in messages


async def test_edit_message(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    new_message: Message = await make_message(database_session, user, group, "First")
    updated_message: Message = await edit_message(database_session, new_message, "First!")
    assert updated_message.message == "First!"


async def test_delete_message(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    message1: Message = await make_message(database_session, user1, group1, "First")
    await make_message(database_session, user1, group1, "Second")
    messages: List[Message] = await get_messages_by_group(database_session, group1)
    assert len(messages) == 2
    await delete_message(database_session, message1)
    messages = await get_messages_by_group(database_session, group1)
    assert len(messages) == 1
