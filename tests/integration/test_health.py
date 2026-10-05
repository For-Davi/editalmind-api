from importlib.metadata import version

import pytest
from httpx import ASGITransport, AsyncClient

from editalmind.infrastructure.settings import Settings
from editalmind.main import create_app

pytestmark = pytest.mark.integration


async def test_health_reports_service_status(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "editalmind-api",
        "version": version("editalmind"),
        "environment": "test",
    }


async def test_openapi_documents_health_route(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    assert "/health" in response.json()["paths"]


async def test_docs_are_hidden_in_production() -> None:
    app = create_app(Settings(_env_file=None, environment="production"))

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        docs = await client.get("/docs")
        health = await client.get("/health")

    assert docs.status_code == 404
    assert health.json()["environment"] == "production"
