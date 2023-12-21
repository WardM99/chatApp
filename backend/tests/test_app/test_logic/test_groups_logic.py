import pytest

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.app.exceptions.alreadyingroup import AlreadyInGroupException
from src.app.exceptions.notingroup import NotInGroupException
from src.app.exceptions.wronguser import WrongUserException
from src.app.logic.groups_logic import (
    logic_add_user,
    logic_add_user_by_name,
    logic_delete_group,
    logic_edit_group_name,
    logic_get_group_by_id,
    logic_make_new_group,
    logic_remove_user,
    logic_tranfer_owner,
    logic_user_in_group
)
from src.database.crud.user import make_user
from src.database.models import User, Group

async def test_logic_make_new_group(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    group: Group = await logic_make_new_group(database_session, owner, "GR1")
    assert group.name == "GR1"
    assert len(group.users) == 1
    assert group.users[0] == owner


async def test_logic_get_group_by_id(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    group: Group = await logic_get_group_by_id(new_group.group_id, database_session)
    assert new_group == group


async def test_logic_edit_group_name(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    await logic_edit_group_name(database_session, owner, new_group, "GR2")
    assert new_group.name == "GR2"


async def test_logic_edit_group_name_wrong_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    with pytest.raises(WrongUserException):
        await logic_edit_group_name(database_session, user2, new_group, "PW2")


async def test_logic_transfer_owner(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    await logic_tranfer_owner(database_session, owner, new_group, user2.user_id)
    assert new_group.owner_id == user2.user_id
    assert new_group.owner_id != owner.user_id


async def test_logic_transfer_owner_not_owner(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    with pytest.raises(WrongUserException):
        await logic_tranfer_owner(database_session, user2, new_group, user2)
    assert new_group.owner_id != user2.user_id
    assert new_group.owner_id == owner.user_id


async def test_logic_delete_group(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    group_id: int = new_group.group_id
    await logic_delete_group(database_session, owner, new_group)
    with pytest.raises(NoResultFound):
        await logic_get_group_by_id(group_id, database_session)


async def test_logic_delete_group_wrong_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    group_id: int = new_group.group_id    
    user2: User = await make_user(database_session, "TestUser", "PW1")
    with pytest.raises(WrongUserException):
        await logic_delete_group(database_session, user2, new_group)
    group: Group = await logic_get_group_by_id(group_id, database_session)
    assert new_group == group


async def test_logic_add_user_by_name(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    await logic_add_user_by_name(database_session, owner, new_group, "TestUser")
    assert len(new_group.users) == 2
    assert new_group.users[1] == user2


async def test_logic_add_user_by_name_wrong_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    with pytest.raises(WrongUserException):
        await logic_add_user_by_name(database_session, user2, new_group, "TestUser")
    assert len(new_group.users) == 1


async def test_logic_add_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    await logic_add_user(database_session, user2, new_group)
    assert len(new_group.users) == 2
    assert new_group.users[1] == user2


async def test_logic_add_user_multiple_times(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW1")
    await logic_add_user(database_session, user2, new_group)
    with pytest.raises(AlreadyInGroupException):
        await logic_add_user(database_session, user2, new_group)
    assert len(new_group.users) == 2


async def test_logic_remove_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW5")
    await logic_add_user(database_session, user2, new_group)
    assert len(new_group.users) == 2
    await logic_remove_user(database_session, owner, new_group, user2.user_id)
    assert len(new_group.users) == 1


async def test_logic_remove_user_same_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW5")
    await logic_add_user(database_session, user2, new_group)
    assert len(new_group.users) == 2
    await logic_remove_user(database_session, user2, new_group, user2.user_id)
    assert len(new_group.users) == 1


async def test_logic_remove_user_wrong_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW5")
    user3: User = await make_user(database_session, "TestUser2", "PW5")
    await logic_add_user(database_session, user2, new_group)
    await logic_add_user(database_session, user3, new_group)
    assert len(new_group.users) == 3
    with pytest.raises(WrongUserException):
        await logic_remove_user(database_session, user2, new_group, user3.user_id)
    assert len(new_group.users) == 3


async def test_logic_user_in_group(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user: User = await logic_user_in_group(owner, new_group)
    assert user == owner


async def test_logic_user_not_in_group(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Jos", "PW1")
    new_group: Group = await logic_make_new_group(database_session, owner, "GR1")
    user2: User = await make_user(database_session, "TestUser", "PW5")
    with pytest.raises(NotInGroupException):
        await logic_user_in_group(user2, new_group)
    await logic_add_user(database_session, user2, new_group)
    user: User = await logic_user_in_group(user2, new_group)
    assert user == user2
