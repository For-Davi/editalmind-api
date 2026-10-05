from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from editalmind.infrastructure.settings import Settings
from editalmind.main import create_app


@pytest.fixture
def settings() -> Settings:
    return Settings(_env_file=None, environment="test")


@pytest.fixture
async def client(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
