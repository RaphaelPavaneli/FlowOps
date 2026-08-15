from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dependencies.autenticacao import get_usuario_atual
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso


def exigir_perfil(
    *perfis_permitidos: PerfilAcesso,
) -> Callable[..., Usuario]:
    """Cria uma dependência que restringe a rota aos perfis informados."""

    def validar_perfil(
        usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    ) -> Usuario:
        if usuario.perfil_acesso not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não possui permissão para executar esta ação.",
            )
        return usuario

    return validar_perfil
