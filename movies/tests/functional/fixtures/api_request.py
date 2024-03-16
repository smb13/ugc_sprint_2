from http import HTTPStatus

import aiohttp
import pytest_asyncio
from settings import test_settings


@pytest_asyncio.fixture(scope="session")
async def session():
    async with aiohttp.ClientSession() as session:
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
