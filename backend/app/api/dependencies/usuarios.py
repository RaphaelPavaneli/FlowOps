from typing import Annotated

from fastapi import Depends

from app.api.dependencies.autenticacao import get_usuario_repository
from app.application.use_cases.alterar_perfil_usuario import AlterarPerfilUsuario
from app.application.use_cases.alterar_status_usuario import AlterarStatusUsuario
from app.application.use_cases.listar_usuarios import ListarUsuarios
from app.domain.repositories.usuario_repository import UsuarioRepository


def get_listar_usuarios(
    repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
) -> ListarUsuarios:
    return ListarUsuarios(repository)


def get_alterar_perfil_usuario(
    repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
) -> AlterarPerfilUsuario:
    return AlterarPerfilUsuario(repository)


def get_alterar_status_usuario(
    repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
) -> AlterarStatusUsuario:
    return AlterarStatusUsuario(repository)
