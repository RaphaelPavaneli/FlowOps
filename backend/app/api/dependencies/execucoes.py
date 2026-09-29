from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.automacoes import get_automacao_repository
from app.api.dependencies.equipes import get_equipe_repository
from app.application.use_cases.buscar_execucao import BuscarExecucao
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.application.use_cases.listar_execucoes import ListarExecucoes
from app.application.services.executor_automacao import ExecutorAutomacao
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.repositories.sql_execucao_repository import (
    SqlExecucaoRepository,
)
from app.infrastructure.executors.executor_teste_controlado import (
    ExecutorTesteControlado,
)


def get_execucao_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> ExecucaoRepository:
    return SqlExecucaoRepository(session)


def get_executor_automacao() -> ExecutorAutomacao:
    return ExecutorTesteControlado()


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
    executor_automacao: Annotated[
        ExecutorAutomacao,
        Depends(get_executor_automacao),
    ],
) -> IniciarExecucao:
    return IniciarExecucao(
        automacao_repository,
        equipe_repository,
        execucao_repository,
        executor_automacao,
    )


def get_listar_execucoes(
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
) -> ListarExecucoes:
    return ListarExecucoes(
        automacao_repository,
        equipe_repository,
        execucao_repository,
    )


def get_buscar_execucao(
    equipe_repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
    execucao_repository: Annotated[
        ExecucaoRepository,
        Depends(get_execucao_repository),
    ],
) -> BuscarExecucao:
    return BuscarExecucao(equipe_repository, execucao_repository)
