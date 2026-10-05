"""Composition root: the only place that wires concrete adapters into the application."""

from importlib.metadata import version

from fastapi import FastAPI

from editalmind.infrastructure.settings import Settings, get_settings
from editalmind.presentation.http import health


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title="EditalMind API",
        version=version("editalmind"),
        debug=settings.debug,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
    )
    app.state.settings = settings
    app.include_router(health.router)
    return app
