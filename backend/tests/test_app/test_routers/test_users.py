
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.crud.user import make_user
from src.database.models import User
from tests.utils.authorization.auth_client import AuthClient

async def test_make_user(test_client: AsyncClient):
    new_user = await test_client.post("/users", json={"name": "Joske", "password": "PW1"})
    assert new_user.status_code == status.HTTP_201_CREATED
    new_user_json = new_user.json()
    assert new_user_json["access_token"]
    assert new_user_json["token_type"] == "bearer"
    assert new_user_json["user"]["name"] == "Joske"
    assert new_user_json["user"]["user_id"]
    assert new_user_json["user"]["status"] is None
    assert len(new_user_json["user"]["groups"]) == 0


async def test_make_user_dublicate(test_client: AsyncClient):
    new_user = await test_client.post("/users", json={"name": "Joske", "password": "PW1"})
    assert new_user.status_code == status.HTTP_201_CREATED
    new_user = await test_client.post("/users", json={"name": "Joske", "password": "PW1"})
    assert new_user.status_code == 400


async def test_make_user_and_login(test_client: AsyncClient):
    new_user = await test_client.post("/users", json={"name": "Joske", "password": "PW1"})
    assert new_user.status_code == status.HTTP_201_CREATED
    login_request = await test_client.post("/users/login", data={"username": "Joske", "password": "PW1", "grant_type": "password"},
                                           headers={"content-type": "application/x-www-form-urlencoded"})
    assert login_request.status_code == status.HTTP_200_OK
    data = login_request.json()
    assert data["user"]["name"] == "Joske"
    assert data["token_type"] == "bearer"
    assert data["access_token"] is not None


async def test_login_fail_wrong_password(test_client: AsyncClient):
    post_request = await test_client.post("/users", json={"name": "New User", "password": "pw"})
    assert post_request.status_code == status.HTTP_201_CREATED
    login_request = await test_client.post("/users/login", data={"username": "New User", "password": "pw5", "grant_type": "password"},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    assert login_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_login_fail_wrong_username(test_client: AsyncClient):
    post_request = await test_client.post("/users", json={"name": "New User", "password": "pw1"})
    assert post_request.status_code == status.HTTP_201_CREATED
    login_request = await test_client.post("/users/login", data={"username": "NewUser", "password": "pw1", "grant_type": "password"},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    print(login_request.json())
    assert login_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user_not_logged_in(test_client: AsyncClient):
    get_request = await test_client.get("/users/1")
    assert get_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    data = await auth_client.post("/users", json={"name": "New User", "password": "pw1"})
    user_id = data.json()["user"]["user_id"]
    auth_client.login(user)
    get_request = await auth_client.get(f"/users/{user_id}")
    data = get_request.json()
    assert get_request.status_code == status.HTTP_200_OK
    assert data["user_id"] == user_id
    assert data["name"] == "New User"
    assert "password" not in data

    get_request = await auth_client.get(f"/users/{user.user_id}")
    data = get_request.json()
    assert get_request.status_code == status.HTTP_200_OK
    assert data["user_id"] == user.user_id
    assert data["name"] == "Joske"
    assert "password" not in data


async def test_delete_user_not_logged_in(test_client: AsyncClient):
    request = await test_client.delete("/users/1")
    assert request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_change_user_not_logged_in(test_client: AsyncClient):
    request = await test_client.put("/users/1", json={"name": "USER1", "password": "PASSWORD"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_change_password_not_logged_in(database_session: AsyncSession, test_client: AsyncClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    request = await test_client.patch(f"/users/{user.user_id}/password", json={"password": "PASSWORD"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_change_name_not_logged_in(database_session: AsyncSession, test_client: AsyncClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    request = await test_client.patch(f"/users/{user.user_id}/name", json={"name": "USER1"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_change_status_not_logged_in(database_session: AsyncSession, test_client: AsyncClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    request = await test_client.patch(f"/users/{user.user_id}/status", json={"status": "USER1"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_change_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user_password: str = user.password
    auth_client.login(user)
    await auth_client.put(f"/users/{user.user_id}", json={"name": "USER1", "password": "PASSWORD"})
    assert user.name == "USER1"
    assert user.password != user_password


async def test_change_user_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user2: User = await make_user(database_session, "USER2", "PW1")
    user_password: str = user2.password
    auth_client.login(user)
    request = await auth_client.put(f"/users/{user2.user_id}", json={"name": "USER1", "password": "PASSWORD"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED
    assert user2.name == "USER2"
    assert user2.password == user_password


async def test_delete_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user_id = user.user_id
    user2: User = await make_user(database_session, "USER2", "PW1")
    auth_client.login(user)
    await auth_client.delete(f"/users/{user.user_id}")
    auth_client.login(user2)
    get_request = await auth_client.get(f"/users/{user_id}")
    assert get_request.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_user_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user2: User = await make_user(database_session, "USER2", "PW1")
    auth_client.login(user)
    request = await auth_client.delete(f"/users/{user2.user_id}")
    assert request.status_code == status.HTTP_401_UNAUTHORIZED
    get_request = await auth_client.get(f"/users/{user2.user_id}")
    assert get_request.status_code == status.HTTP_200_OK
    assert get_request.json()["name"] == user2.name


async def test_change_user_password(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user_password = user.password
    auth_client.login(user)
    request = await auth_client.patch(f"/users/{user.user_id}/password", json={"password": "PW2"})
    assert request.status_code == status.HTTP_204_NO_CONTENT
    assert user.password != user_password


async def test_change_user_password_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user2: User = await make_user(database_session, "USER2", "PW1")
    user_password = user2.password
    auth_client.login(user)
    request = await auth_client.patch(f"/users/{user2.user_id}/password", json={"password": "PW2"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED
    assert user2.password == user_password


async def test_change_user_name(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    auth_client.login(user)
    request = await auth_client.patch(f"/users/{user.user_id}/name", json={"name": "PW2"})
    assert request.status_code == status.HTTP_204_NO_CONTENT
    assert user.name == "PW2"


async def test_change_user_name_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user2: User = await make_user(database_session, "USER2", "PW1")
    user_name = user2.name
    auth_client.login(user)
    request = await auth_client.patch(f"/users/{user2.user_id}/name", json={"name": "PW2"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED
    assert user2.name == user_name


async def test_change_user_status(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    auth_client.login(user)
    request = await auth_client.patch(f"/users/{user.user_id}/status", json={"status": "Writing code"})
    assert request.status_code == status.HTTP_204_NO_CONTENT
    assert user.status == "Writing code"


async def test_change_user_status_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "Joske", "PW1")
    user2: User = await make_user(database_session, "USER2", "PW1")
    auth_client.login(user)
    request = await auth_client.patch(f"/users/{user2.user_id}/status", json={"status": "Writing code"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED
    assert user2.status is None
