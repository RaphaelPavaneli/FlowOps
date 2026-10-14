from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.api.dependencies.execucoes import (
    encerrar_despachante_execucao,
    recuperar_execucoes_interrompidas,
)
from app.api.router import api_router
from app.core.config import settings


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    gerenciar_execucoes = application.state.gerenciar_execucoes_no_lifespan
    if gerenciar_execucoes:
        recuperadas = recuperar_execucoes_interrompidas()
        if recuperadas:
            logger.warning(
                "Execuções interrompidas foram recuperadas na inicialização.",
                extra={"quantidade_execucoes": recuperadas},
            )

    try:
        yield
    finally:
        if gerenciar_execucoes:
            encerrar_despachante_execucao()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        lifespan=lifespan,
    )
    application.state.gerenciar_execucoes_no_lifespan = True
    application.include_router(api_router, prefix=settings.app.api_v1_prefix)
    return application


app = create_app()
