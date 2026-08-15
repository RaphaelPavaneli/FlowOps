from uuid import UUID

from app.domain.entities.usuario import Usuario
from app.domain.exceptions.autenticacao import (
    UsuarioInativoError,
    UsuarioNaoEncontradoError,
)
from app.domain.repositories.usuario_repository import UsuarioRepository


class ObterUsuarioAtual:
    """Obtém o usuário do token e confirma seu estado atual no banco."""

    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self._usuario_repository = usuario_repository

    def executar(self, usuario_id: UUID) -> Usuario:
        usuario = self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError
        if not usuario.ativo:
            raise UsuarioInativoError
        return usuario
