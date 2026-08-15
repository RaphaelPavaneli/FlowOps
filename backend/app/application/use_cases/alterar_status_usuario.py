from datetime import datetime, timezone
from uuid import UUID

from app.domain.entities.usuario import Usuario
from app.domain.exceptions.autenticacao import (
    OperacaoUsuarioNaoPermitidaError,
    UsuarioNaoEncontradoError,
)
from app.domain.repositories.usuario_repository import UsuarioRepository


class AlterarStatusUsuario:
    """Ativa ou desativa usuários sem bloquear o administrador atual."""

    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self._usuario_repository = usuario_repository

    def executar(
        self,
        administrador_id: UUID,
        usuario_id: UUID,
        ativo: bool,
    ) -> Usuario:
        if administrador_id == usuario_id and not ativo:
            raise OperacaoUsuarioNaoPermitidaError

        usuario = self._usuario_repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontradoError

        usuario.ativo = ativo
        usuario.atualizado_em = datetime.now(timezone.utc)
        atualizado = self._usuario_repository.atualizar(usuario)
        if atualizado is None:
            raise UsuarioNaoEncontradoError
        return atualizado
