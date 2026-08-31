from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.autenticacao import get_usuario_repository
from app.application.use_cases.associar_usuario_equipe import (
    AssociarUsuarioEquipe,
)
from app.application.use_cases.criar_equipe import CriarEquipe
from app.application.use_cases.listar_equipes import ListarEquipes
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.repositories.sql_equipe_repository import (
    SqlEquipeRepository,
)


def get_equipe_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> EquipeRepository:
    return SqlEquipeRepository(session)


def get_criar_equipe(
    repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
) -> CriarEquipe:
    return CriarEquipe(repository)


def get_listar_equipes(
    repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
) -> ListarEquipes:
    return ListarEquipes(repository)


def get_associar_usuario_equipe(
    equipe_repository: Annotated[
        EquipeRepository,
        Depends(get_equipe_repository),
    ],
    usuario_repository: Annotated[
        UsuarioRepository,
        Depends(get_usuario_repository),
    ],
) -> AssociarUsuarioEquipe:
    return AssociarUsuarioEquipe(equipe_repository, usuario_repository)
