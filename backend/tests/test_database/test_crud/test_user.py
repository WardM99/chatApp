import pytest 

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.database.models import User
from src.database.crud.user import(
    get_user_by_id,
    make_user,
    edit_user_password,
    edit_user_name,
    delete_user,
    get_user_by_name
)

async def test_make_user(database_session: AsyncSession):
    """Test to make and get a user"""
    new_user: User = await make_user(database_session, "Joske", "PW1")
    assert new_user.name == "Joske"
    assert new_user.password == "PW1"
    assert new_user.groups == []


async def test_make_user_dublicate(database_session: AsyncSession):
    """Test to make and get a dublicate user"""
    await make_user(database_session, "Joske", "PW1")
    with pytest.raises(IntegrityError):
        await make_user(database_session, "Joske", "pw2")


async def test_get_user(database_session: AsyncSession):
    new_user: User = await make_user(database_session, "Joske", "PW1")
    user: User = await get_user_by_id(database_session, new_user.user_id)
    assert user == new_user


async def test_delete_user(database_session: AsyncSession):
    new_user: User = await make_user(database_session, "Joske", "PW1")
    await delete_user(database_session, new_user)

    with pytest.raises(NoResultFound):
        await get_user_by_id(database_session, new_user.user_id)

    with pytest.raises(NoResultFound):
        await get_user_by_name(database_session, new_user.name)


async def test_update_password(database_session: AsyncSession):
    new_user: User = await make_user(database_session, "Joske", "PW1")
    edit_user: User = await edit_user_password(database_session, new_user, "PW2")
    assert edit_user.password == "PW2"


async def test_update_name(database_session: AsyncSession):
    new_user: User = await make_user(database_session, "Hoske", "PW1")
    edit_user: User = await edit_user_name(database_session, new_user, "Joske")
    assert edit_user.name == "Joske"


async def test_get_user_by_name(database_session: AsyncSession):
    new_user: User = await make_user(database_session, "Joske", "PW1")
    user: User = await get_user_by_name(database_session, new_user.name)
    assert user == new_user
