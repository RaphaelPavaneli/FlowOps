from datetime import datetime, timezone
from uuid import UUID

from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.exceptions.autenticacao import (
    OperacaoUsuarioNaoPermitidaError,
    UsuarioNaoEncontradoError,
)
from app.domain.repositories.usuario_repository import UsuarioRepository


class AlterarPerfilUsuario:
    """Altera o perfil sem permitir o auto-rebaixamento administrativo."""

    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self._usuario_repository = usuario_repository

    def executar(
        self,
        administrador_id: UUID,
        usuario_id: UUID,
        perfil_acesso: PerfilAcesso,
    ) -> Usuario:
        if (
            administrador_id == usuario_id
            and perfil_acesso != PerfilAcesso.ADMINISTRADOR
        ):
            raise OperacaoUsuarioNaoPermitidaError

        usuario = self._usuario_repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontradoError

        usuario.perfil_acesso = perfil_acesso
        usuario.atualizado_em = datetime.now(timezone.utc)
        atualizado = self._usuario_repository.atualizar(usuario)
        if atualizado is None:
            raise UsuarioNaoEncontradoError
        return atualizado
