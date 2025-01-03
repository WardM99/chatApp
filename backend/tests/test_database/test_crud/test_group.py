import pytest

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.database.models import User, Group
from src.database.crud.group import(
    get_group_by_id,
    make_group,
    edit_group_name,
    transfer_owner,
    delete_group,
    add_user,
    remove_user
)
from src.database.crud.user import make_user


async def test_make_group(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1")
    assert new_group.owner_id == owner.user_id
    assert new_group.name == "Group1"
    assert len(new_group.users) == 1
    assert new_group.users[0] == owner
    assert new_group.is_private is False


async def test_make_group_empty_name(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    with pytest.raises(ValueError):
        await make_group(database_session, owner, "")


async def test_make_group_is_private(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1", is_private=True)
    assert new_group.owner_id == owner.user_id
    assert new_group.name == "Group1"
    assert len(new_group.users) == 1
    assert new_group.users[0] == owner
    assert new_group.is_private


async def test_make_group_public(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1", is_private=False)
    assert new_group.owner_id == owner.user_id
    assert new_group.name == "Group1"
    assert len(new_group.users) == 1
    assert new_group.users[0] == owner
    assert new_group.is_private is False


async def test_get_group_by_id(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1")
    group: Group = await get_group_by_id(database_session, new_group.group_id)
    assert new_group == group


async def test_get_group_by_id_dont_exist(database_session: AsyncSession): 
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1")
    with pytest.raises(NoResultFound):
        await get_group_by_id(database_session, new_group.group_id+1)


async def test_edit_group_name(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Soup1")
    group: Group = await edit_group_name(database_session, new_group, "Group1")
    assert group.name == "Group1"


async def test_edit_group_name_empty_name(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Soup1")
    with pytest.raises(ValueError):
        await edit_group_name(database_session, new_group, "")

async def test_tranfer_owner(database_session: AsyncSession):
    old_owner: User = await make_user(database_session, "Old", "pw1")
    new_owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, old_owner, "Group1")
    group: Group = await transfer_owner(database_session, new_group, new_owner)
    assert group.owner_id == new_owner.user_id


async def test_delete_group(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1")
    await delete_group(database_session, new_group)
    with pytest.raises(NoResultFound):
        await get_group_by_id(database_session, new_group.group_id)


async def test_add_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    user2: User = await make_user(database_session, "User2", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1")
    group: Group = await add_user(database_session, new_group, user2)
    assert len(group.users) == 2
    assert group.users[1] == user2


async def test_remove_user(database_session: AsyncSession):
    owner: User = await make_user(database_session, "Owner", "pw1")
    user1: User = await make_user(database_session, "User1", "pw1")
    user2: User = await make_user(database_session, "User2", "pw1")
    new_group: Group = await make_group(database_session, owner, "Group1")
    await add_user(database_session, new_group, user1)
    group: Group = await add_user(database_session, new_group, user2)
    assert len(group.users) == 3
    group = await remove_user(database_session, group, user2)
    assert len(group.users) == 2
    