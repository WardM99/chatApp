from typing import Text

from requests import Response
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


from src.app.logic.users_logic import create_token
from src.database.models import User

class AuthClient(AsyncClient):
    """Custom TestClient that handles authentication to make tests more compact"""
    user: User | None = None
    headers: dict[str, str] | None = None
    session: AsyncSession

    def __init__(self, session: AsyncSession, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session

    def invalid(self):
        """Sign in with an invalid access token"""
        self.headers = {
            "Authorization": "Bearer I would have been here sooner but the bus kept stopping for other people to get on it"
        }

    def login(self, user: User):
        """Sign in as a user for all future requests"""
        self.user = user

        # Since an authclient is created for every test, the access_token will most likely not run out
        access_token = create_token(user)

        # Add auth headers into dict
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def delete(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().delete(url, **kwargs)

    async def get(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().get(url, **kwargs)

    async def patch(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().patch(url, **kwargs)

    async def post(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().post(url, **kwargs)

    async def put(self, url: Text | None, **kwargs) -> Response:
        if self.headers is not None:
            kwargs["headers"] = self.headers

        return await super().put(url, **kwargs)
