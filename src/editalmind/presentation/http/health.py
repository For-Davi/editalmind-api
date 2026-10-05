from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from editalmind.infrastructure.settings import Environment, Settings
from editalmind.presentation.http.dependencies import get_app_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    environment: Environment


@router.get("/health")
async def health(
    request: Request,
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="editalmind-api",
        version=request.app.version,
        environment=settings.environment,
    )
