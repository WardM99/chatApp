from typing import List

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.exceptions.wronguser import WrongUserException
from src.app.logic.messages_logic import (
    logic_delete_message,
    logic_edit_message,
    logic_get_messages_by_group,
    logic_get_messages_by_user_in_group,
    logic_make_message
)
from src.database.crud.user import make_user
from src.database.crud.group import make_group
from src.database.models import User, Group, Message

async def test_logic_make_message(database_session: AsyncSession):
    user: User = await make_user(database_session, "user1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    message: Message = await logic_make_message(database_session, user, group, "message1")
    assert message.message == "message1"


async def test_logic_get_messages_by_user_in_group(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    user2: User = await make_user(database_session, "User2", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    group2: Group = await make_group(database_session, user1, "Group2")
    message1: Message = await logic_make_message(database_session, user1, group1, "First")
    message2: Message = await logic_make_message(database_session, user1, group1, "Second")
    message3: Message = await logic_make_message(database_session, user2, group1, "3th")
    message4: Message = await logic_make_message(database_session, user1, group2, "4th")

    messages: List[Message] = await logic_get_messages_by_user_in_group(database_session, user1, group1)
    assert len(messages) == 2
    assert message1 in messages
    assert message2 in messages
    assert message3 not in messages
    assert message4 not in messages


async def test_logic_get_messages_by_group(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    user2: User = await make_user(database_session, "User2", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    group2: Group = await make_group(database_session, user1, "Group2")
    message1: Message = await logic_make_message(database_session, user1, group1, "First")
    message2: Message = await logic_make_message(database_session, user1, group1, "Second")
    message3: Message = await logic_make_message(database_session, user2, group1, "3th")
    message4: Message = await logic_make_message(database_session, user1, group2, "4th")

    messages: List[Message] = await logic_get_messages_by_group(database_session, group1)
    assert len(messages) == 3
    assert message1 in messages
    assert message2 in messages
    assert message3 in messages
    assert message4 not in messages
    

async def test_edit_message(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    new_message: Message = await logic_make_message(database_session, user, group, "First")
    updated_message: Message = await logic_edit_message(database_session, new_message, "First!", user)
    assert updated_message.message == "First!"
    

async def test_edit_message_wrong_user(database_session: AsyncSession):
    user: User = await make_user(database_session, "Owner", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    new_message: Message = await logic_make_message(database_session, user, group, "First")
    user2: User = await make_user(database_session, "user2", "pw1")
    with pytest.raises(WrongUserException):
        await logic_edit_message(database_session, new_message, "First!", user2)
    assert new_message.message == "First"


async def test_delete_message(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    message1: Message = await logic_make_message(database_session, user1, group1, "First")
    await logic_make_message(database_session, user1, group1, "Second")
    messages: List[Message] = await logic_get_messages_by_group(database_session, group1)
    assert len(messages) == 2
    await logic_delete_message(database_session, message1, user1)
    messages = await logic_get_messages_by_group(database_session, group1)
    assert len(messages) == 1


async def test_delete_message_wrong_user(database_session: AsyncSession):
    user1: User = await make_user(database_session, "Owner", "pw1")
    group1: Group = await make_group(database_session, user1, "Group1")
    message1: Message = await logic_make_message(database_session, user1, group1, "First")
    await logic_make_message(database_session, user1, group1, "Second")
    messages: List[Message] = await logic_get_messages_by_group(database_session, group1)
    assert len(messages) == 2
    user2: User = await make_user(database_session, "User2", "pw1")
    with pytest.raises(WrongUserException):
        await logic_delete_message(database_session, message1, user2)
    messages = await logic_get_messages_by_group(database_session, group1)
    assert len(messages) == 2
