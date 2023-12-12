
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from tests.utils.authorization.auth_client import AuthClient

"""
async def test_iets(database_session: AsyncSession, auth_client: AuthClient):
    post_request = await auth_client.post("/users", json={"name": "New User", "password": "pw"})
    print(post_request.json())
    assert False
"""
 