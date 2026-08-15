from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
