from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
    )
    application.include_router(api_router, prefix=settings.app.api_v1_prefix)
    return application


app = create_app()
