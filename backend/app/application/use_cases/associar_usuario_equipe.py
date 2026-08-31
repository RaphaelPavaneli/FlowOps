from datetime import datetime, timezone
from uuid import UUID

from app.domain.entities.usuario import Usuario
from app.domain.exceptions.autenticacao import UsuarioNaoEncontradoError
from app.domain.exceptions.equipes import (
    EquipeInativaError,
    EquipeNaoEncontradaError,
)
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.usuario_repository import UsuarioRepository


class AssociarUsuarioEquipe:
    """Associa um usuário a uma equipe ativa por decisão administrativa."""

    def __init__(
        self,
        equipe_repository: EquipeRepository,
        usuario_repository: UsuarioRepository,
    ) -> None:
        self._equipe_repository = equipe_repository
        self._usuario_repository = usuario_repository

    def executar(self, equipe_id: UUID, usuario_id: UUID) -> Usuario:
        equipe = self._equipe_repository.buscar_por_id(equipe_id)
        if equipe is None:
            raise EquipeNaoEncontradaError
        if not equipe.ativa:
            raise EquipeInativaError

        usuario = self._usuario_repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontradoError

        usuario.equipe_id = equipe.id
        usuario.atualizado_em = datetime.now(timezone.utc)
        atualizado = self._usuario_repository.atualizar(usuario)
        if atualizado is None:
            raise UsuarioNaoEncontradoError
        return atualizado
