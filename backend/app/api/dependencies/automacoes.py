from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.equipes import get_equipe_repository
from app.application.use_cases.criar_automacao import CriarAutomacao
from app.application.use_cases.listar_automacoes import ListarAutomacoes
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.repositories.sql_automacao_repository import (
    SqlAutomacaoRepository,
)


def get_automacao_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> AutomacaoRepository:
    return SqlAutomacaoRepository(session)


def get_criar_automacao(
    automacao_repository: Annotated[
        AutomacaoRepository,
        Depends(get_automacao_repository),
    ],
    equipe_repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
) -> CriarAutomacao:
    return CriarAutomacao(automacao_repository, equipe_repository)


def get_listar_automacoes(
    automacao_repository: Annotated[
        AutomacaoRepository,
        Depends(get_automacao_repository),
    ],
    equipe_repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
) -> ListarAutomacoes:
    return ListarAutomacoes(automacao_repository, equipe_repository)
