from math import ceil
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.autorizacao import exigir_perfil
from app.api.dependencies.usuarios import (
    get_alterar_perfil_usuario,
    get_alterar_status_usuario,
    get_listar_usuarios,
)
from app.api.schemas.autenticacao import UsuarioResponse
from app.api.schemas.usuarios import (
    AlterarPerfilRequest,
    AlterarStatusRequest,
    ListaUsuariosResponse,
)
from app.application.use_cases.alterar_perfil_usuario import AlterarPerfilUsuario
from app.application.use_cases.alterar_status_usuario import AlterarStatusUsuario
from app.application.use_cases.listar_usuarios import ListarUsuarios
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.exceptions.autenticacao import (
    OperacaoUsuarioNaoPermitidaError,
    UsuarioNaoEncontradoError,
)


router = APIRouter(prefix="/usuarios", tags=["Usuários"])
administrador_required = exigir_perfil(PerfilAcesso.ADMINISTRADOR)


@router.get(
    "",
    response_model=ListaUsuariosResponse,
    summary="Listar usuários",
)
def listar_usuarios(
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[ListarUsuarios, Depends(get_listar_usuarios)],
    pagina: Annotated[int, Query(ge=1)] = 1,
    itens_por_pagina: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ListaUsuariosResponse:
    resultado = caso_de_uso.executar(pagina, itens_por_pagina)
    return ListaUsuariosResponse(
        usuarios=[
            UsuarioResponse.model_validate(usuario)
            for usuario in resultado.usuarios
        ],
        pagina=resultado.pagina,
        itens_por_pagina=resultado.itens_por_pagina,
        total=resultado.total,
        total_paginas=ceil(resultado.total / resultado.itens_por_pagina),
    )


@router.patch(
    "/{usuario_id}/perfil",
    response_model=UsuarioResponse,
    summary="Alterar perfil de acesso",
)
def alterar_perfil_usuario(
    usuario_id: UUID,
    dados: AlterarPerfilRequest,
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[
        AlterarPerfilUsuario,
        Depends(get_alterar_perfil_usuario),
    ],
) -> UsuarioResponse:
    try:
        usuario = caso_de_uso.executar(
            administrador.id,
            usuario_id,
            dados.perfil_acesso,
        )
    except UsuarioNaoEncontradoError as erro:
        raise _usuario_nao_encontrado() from erro
    except OperacaoUsuarioNaoPermitidaError as erro:
        raise _operacao_nao_permitida() from erro
    return UsuarioResponse.model_validate(usuario)


@router.patch(
    "/{usuario_id}/status",
    response_model=UsuarioResponse,
    summary="Ativar ou desativar usuário",
)
def alterar_status_usuario(
    usuario_id: UUID,
    dados: AlterarStatusRequest,
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[
        AlterarStatusUsuario,
        Depends(get_alterar_status_usuario),
    ],
) -> UsuarioResponse:
    try:
        usuario = caso_de_uso.executar(
            administrador.id,
            usuario_id,
            dados.ativo,
        )
    except UsuarioNaoEncontradoError as erro:
        raise _usuario_nao_encontrado() from erro
    except OperacaoUsuarioNaoPermitidaError as erro:
        raise _operacao_nao_permitida() from erro
    return UsuarioResponse.model_validate(usuario)


def _usuario_nao_encontrado() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuário não encontrado.",
    )


def _operacao_nao_permitida() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Você não pode remover o próprio acesso administrativo.",
    )
