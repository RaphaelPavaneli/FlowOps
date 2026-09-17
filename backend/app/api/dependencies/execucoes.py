from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.automacoes import get_automacao_repository
from app.api.dependencies.equipes import get_equipe_repository
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.repositories.sql_execucao_repository import (
    SqlExecucaoRepository,
)


def get_execucao_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> ExecucaoRepository:
    return SqlExecucaoRepository(session)


def get_iniciar_execucao(
    automacao_repository: Annotated[
        AutomacaoRepository,
        Depends(get_automacao_repository),
    ],
    equipe_repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
    execucao_repository: Annotated[
        ExecucaoRepository,
        Depends(get_execucao_repository),
    ],
) -> IniciarExecucao:
    return IniciarExecucao(
        automacao_repository,
        equipe_repository,
        execucao_repository,
    )
