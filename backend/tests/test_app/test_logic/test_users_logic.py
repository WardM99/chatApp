import pytest

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.database.models import User
from src.app.exceptions.wrongcredentials import WrongCredentialsException
from src.app.exceptions.wronguser import WrongUserException
from src.app.logic.users_logic import(
    logic_make_new_user,
    logic_get_user_by_name_and_password,
    logic_get_user_by_id,
    logic_change_password,
    logic_change_name,
    logic_delete_user,
    logic_change_user
)


async def test_logic_make_new_user(database_session: AsyncSession):
    user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    assert user.name == "Joske"
    assert user.password != "PW1"


async def test_logic_get_user_by_name_and_password(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    user: User = await logic_get_user_by_name_and_password(database_session, "Joske", "PW1")
    assert user == new_user


async def test_logic_get_user_by_name_and_password_wrong_password(database_session: AsyncSession):
    await logic_make_new_user(database_session, "Joske", "PW1")
    with pytest.raises(WrongCredentialsException):
        await logic_get_user_by_name_and_password(database_session, "Joske", "PW2")


async def test_logic_get_user_by_name_and_password_wrong_name(database_session: AsyncSession):
    await logic_make_new_user(database_session, "Joske", "PW1")
    with pytest.raises(WrongCredentialsException):
        await logic_get_user_by_name_and_password(database_session, "Joska", "PW1")


async def test_logic_get_user_by_id(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    user: User = await logic_get_user_by_id(database_session, new_user.user_id)

    assert user == new_user


async def test_logic_change_name(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    await logic_change_name(database_session, new_user, new_user.user_id, "Ruth")
    assert new_user.name != "Joske"
    assert new_user.name == "Ruth"


async def test_logic_change_name_wrong_id(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    with pytest.raises(WrongUserException):
        await logic_change_name(database_session, new_user, new_user.user_id + 1, "Ruth")
    assert new_user.name == "Joske"
    assert new_user.name != "Ruth"


async def test_logic_change_password(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    old_password: str = new_user.password
    await logic_change_password(database_session, new_user, new_user.user_id, "PW2")
    assert new_user.password != old_password


async def test_logic_change_password_wrong_id(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    old_password: str = new_user.password
    with pytest.raises(WrongUserException):
        await logic_change_password(database_session, new_user, new_user.user_id + 1, "PW2")
    assert new_user.password == old_password


async def test_logic_delete_user(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    await logic_delete_user(database_session, new_user, new_user.user_id)
    with pytest.raises(NoResultFound):
        await logic_get_user_by_id(database_session, new_user.user_id)


async def test_logic_delete_user_wrong_id(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    with pytest.raises(WrongUserException):
        await logic_delete_user(database_session, new_user, new_user.user_id+1)
    user: User = await logic_get_user_by_id(database_session, new_user.user_id)
    assert user == new_user


async def test_logic_change_user(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    old_password: str = new_user.password
    await logic_change_user(database_session, new_user, new_user.user_id, "Ruth", "PW2")
    assert new_user.name == "Ruth"
    assert new_user.password != old_password


async def test_logic_change_user_no_password(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    old_password: str = new_user.password
    await logic_change_user(database_session, new_user, new_user.user_id, "Ruth", None)
    assert new_user.name == "Ruth"
    assert new_user.password == old_password


async def test_logic_change_user_no_name(database_session: AsyncSession):
    new_user: User = await logic_make_new_user(database_session, "Joske", "PW1")
    old_password: str = new_user.password
    await logic_change_user(database_session, new_user, new_user.user_id, None, "PW2")
    assert new_user.name == "Joske"
    assert new_user.password != old_password
