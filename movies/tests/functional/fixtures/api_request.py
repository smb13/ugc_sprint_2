from http import HTTPStatus
from uuid import uuid4

from async_fastapi_jwt_auth import AuthJWT

import aiohttp
import pytest_asyncio
from settings import test_settings, authjwt_settings


@AuthJWT.load_config
def get_config():
    return authjwt_settings


@pytest_asyncio.fixture(scope="session")
async def session():
    jwt = AuthJWT()
    access_token = await jwt.create_access_token(subject=str(uuid4()),
                                                 user_claims={"sub": "username:user@yandex.ru", "roles": ["user"]})
    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {access_token}"}) as session:
        yield session


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(path: str, params: dict | None = None, expected_status: HTTPStatus = HTTPStatus.OK):
        url = test_settings.service_url + path
        async with session.get(url, params=params) as response:
            body = await response.json()
            status = response.status
        if status != expected_status:
            raise ValueError(f"Expected response status {expected_status}, got {status}: {body}")
        return body

    return inner
