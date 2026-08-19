from fastapi import APIRouter, status

from app.api.schemas.health import HealthResponse
from app.core.config import settings


router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API health",
)
def get_health() -> HealthResponse:
    """Return the current API status."""
    return HealthResponse(
        status="ok",
        service=settings.app.name,
        version=settings.app.version,
    )
