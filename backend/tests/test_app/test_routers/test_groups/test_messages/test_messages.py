from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.crud.user import make_user
from src.database.crud.group import make_group
from src.database.models import User, Group
from tests.utils.authorization.auth_client import AuthClient

async def test_make_message(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    assert data["message_id"]
    assert data["message"] == "Hi"
    assert data["reply_id"] is None
    assert data["sender_id"] == user.user_id
    assert data["group_id"] == group.group_id


async def test_make_reply(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data_firest_message = post_request.json()
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "How are you", "reply_id": data_firest_message["message_id"]})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    assert data["message_id"]
    assert data["message"] == "How are you"
    assert data["reply_id"] == data_firest_message["message_id"]
    assert data["sender_id"] == user.user_id
    assert data["group_id"] == group.group_id


async def test_make_message_not_logged_in(database_session: AsyncSession, test_client: AsyncClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    post_request = await test_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_messages_in_group(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "How are yall", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["messages"]) == 2


async def test_get_messages_in_group_not_logged_in(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "How are yall", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    auth_client.invalid()
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_messages_in_group_by_name(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    user2: User = await make_user(database_session, "User2", "pw2")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "How are yall", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    auth_client.login(user2)
    await auth_client.put(f"/groups/{group.group_id}/user")
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages/{user.name}")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["messages"]) == 2
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages/{user2.name}")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["messages"]) == 1


async def test_get_messages_in_group_by_name_not_logged_in(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    user2: User = await make_user(database_session, "User2", "pw2")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "How are yall", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    auth_client.login(user2)
    await auth_client.put(f"/groups/{group.group_id}/user")
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    auth_client.invalid()
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages/{user.name}")
    assert get_request.status_code == status.HTTP_401_UNAUTHORIZED
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages/{user2.name}")
    assert get_request.status_code == status.HTTP_401_UNAUTHORIZED


async def test_change_message(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    message_id = data["message_id"]
    put_request = await auth_client.put(f"/groups/{group.group_id}/messages/{message_id}", json={"message": "Hi!", "reply_id": None})
    assert put_request.status_code == status.HTTP_204_NO_CONTENT
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert data["messages"][0]["message"] == "Hi!"


async def test_change_message_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    message_id = data["message_id"]
    user2: User = await make_user(database_session, "User2", "pw1")
    auth_client.login(user2)
    await auth_client.put(f"/groups/{group.group_id}/user")
    put_request = await auth_client.put(f"/groups/{group.group_id}/messages/{message_id}", json={"message": "Hi!", "reply_id": None})
    assert put_request.status_code == status.HTTP_401_UNAUTHORIZED
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert data["messages"][0]["message"] == "Hi"


async def test_change_message_not_logged_in(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    message_id = data["message_id"]
    auth_client.invalid()
    put_request = await auth_client.put(f"/groups/{group.group_id}/messages/{message_id}", json={"message": "Hi!", "reply_id": None})
    assert put_request.status_code == status.HTTP_401_UNAUTHORIZED
    auth_client.login(user)
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert data["messages"][0]["message"] == "Hi"


async def test_delete_message(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    message_id = data["message_id"]
    delete_request = await auth_client.delete(f"/groups/{group.group_id}/messages/{message_id}")
    assert delete_request.status_code == status.HTTP_204_NO_CONTENT
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["messages"]) == 0


async def test_delete_message_wrong_user(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    message_id = data["message_id"]
    user2: User = await make_user(database_session, "User2", "pw1")
    auth_client.login(user2)
    await auth_client.put(f"/groups/{group.group_id}/user")
    delete_request = await auth_client.delete(f"/groups/{group.group_id}/messages/{message_id}")
    assert delete_request.status_code == status.HTTP_401_UNAUTHORIZED
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["messages"]) == 1


async def test_delete_message_not_logged_in(database_session: AsyncSession, auth_client: AuthClient):
    user: User = await make_user(database_session, "User1", "pw1")
    group: Group = await make_group(database_session, user, "Group1")
    auth_client.login(user)
    post_request = await auth_client.post(f"/groups/{group.group_id}/messages", json={"message": "Hi", "reply_id": None})
    assert post_request.status_code == status.HTTP_201_CREATED
    data = post_request.json()
    message_id = data["message_id"]
    auth_client.invalid()
    delete_request = await auth_client.delete(f"/groups/{group.group_id}/messages/{message_id}")
    assert delete_request.status_code == status.HTTP_401_UNAUTHORIZED
    auth_client.login(user)
    get_request = await auth_client.get(f"/groups/{group.group_id}/messages")
    assert get_request.status_code == status.HTTP_200_OK
    data = get_request.json()
    assert len(data["messages"]) == 1