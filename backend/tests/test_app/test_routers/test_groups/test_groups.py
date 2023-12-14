
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.crud.user import make_user
from src.database.models import User
from tests.utils.authorization.auth_client import AuthClient


async def test_make_group(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    auth_client.login(user)
    post_request = await auth_client.post("/groups", json={"name": "Cool Group"})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    assert "group_id" in data
    assert data["name"] == "Cool Group"
    assert data["owner_id"] == user.user_id
    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "User1"
    assert data["users"][0]["user_id"] == user.user_id
    assert "password" not in data["users"][0]


async def test_make_group_not_logged_in(database_session: AsyncSession, test_client: AsyncClient):
    post_request = await test_client.post("/groups", json={"name": "Cool Group"})
    assert post_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_group_by_id_not_logged_in(database_session: AsyncSession, test_client: AsyncClient, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    auth_client.login(user)
    post_request = await auth_client.post("/groups", json={"name": "Cool Group"})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    group_id = data["group_id"]
    get_request = await test_client.get(f"/groups/{group_id}")
    assert get_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_group_by_id(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    auth_client.login(user)
    post_request = await auth_client.post("/groups", json={"name": "Cool Group"})
    assert post_request.status_code == status.HTTP_201_CREATED
    data_post = post_request.json()
    group_id = data_post["group_id"]
    get_request = await auth_client.get(f"/groups/{group_id}")
    assert get_request.status_code == status.HTTP_200_OK
    data_get = get_request.json()
    assert data_post == data_get


async def test_get_group_by_id_dont_excist(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    auth_client.login(user)
    post_request = await auth_client.post("/groups", json={"name": "Cool Group"})
    assert post_request.status_code == status.HTTP_201_CREATED
    data_post = post_request.json()
    group_id = data_post["group_id"]
    get_request = await auth_client.get(f"/groups/{group_id+1}")
    assert get_request.status_code == status.HTTP_404_NOT_FOUND
