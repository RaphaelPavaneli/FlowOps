from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.automacoes import get_automacao_repository
from app.api.dependencies.equipes import get_equipe_repository
from app.application.use_cases.buscar_execucao import BuscarExecucao
from app.application.use_cases.cancelar_execucao import CancelarExecucao
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.application.use_cases.listar_execucoes import ListarExecucoes
from app.application.use_cases.recuperar_execucoes_interrompidas import (
    RecuperarExecucoesInterrompidas,
)
from app.application.services.executor_automacao import ExecutorAutomacao
from app.application.services.despachante_execucao import DespachanteExecucao
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.database.connection import SessionLocal, get_db_session
from app.infrastructure.database.repositories.sql_execucao_repository import (
    SqlExecucaoRepository,
)
from app.infrastructure.executors.executor_teste_controlado import (
    ExecutorTesteControlado,
)
from app.infrastructure.executors.despachante_execucao_local import (
    DespachanteExecucaoLocal,
)


_executor_automacao = ExecutorTesteControlado()
_despachante_execucao = DespachanteExecucaoLocal(
    SessionLocal,
    _executor_automacao,
)


def get_execucao_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> ExecucaoRepository:
    return SqlExecucaoRepository(session)


def get_executor_automacao() -> ExecutorAutomacao:
    return _executor_automacao


def get_despachante_execucao() -> DespachanteExecucao:
    return _despachante_execucao


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
    despachante_execucao: Annotated[
        DespachanteExecucao,
        Depends(get_despachante_execucao),
    ],
) -> IniciarExecucao:
    return IniciarExecucao(
        automacao_repository,
        equipe_repository,
        execucao_repository,
        despachante_execucao,
    )


def get_cancelar_execucao(
    equipe_repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
    execucao_repository: Annotated[
        ExecucaoRepository,
        Depends(get_execucao_repository),
    ],
    despachante_execucao: Annotated[
        DespachanteExecucao,
        Depends(get_despachante_execucao),
    ],
) -> CancelarExecucao:
    return CancelarExecucao(
        equipe_repository,
        execucao_repository,
        despachante_execucao,
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


def recuperar_execucoes_interrompidas() -> int:
    """Recupera estados ativos antes de aceitar novas requisições."""
    with SessionLocal() as session:
        return RecuperarExecucoesInterrompidas(
            SqlExecucaoRepository(session)
        ).executar()


def encerrar_despachante_execucao() -> None:
    """Encerra threads e subprocessos pertencentes à instância local."""
    _despachante_execucao.encerrar()
