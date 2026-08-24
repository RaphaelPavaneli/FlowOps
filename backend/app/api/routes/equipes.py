from math import ceil
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.autorizacao import exigir_perfil
from app.api.dependencies.equipes import (
    get_associar_usuario_equipe,
    get_criar_equipe,
    get_listar_equipes,
)
from app.api.schemas.autenticacao import UsuarioResponse
from app.api.schemas.equipes import (
    CriarEquipeRequest,
    EquipeResponse,
    ListaEquipesResponse,
)
from app.application.use_cases.associar_usuario_equipe import (
    AssociarUsuarioEquipe,
)
from app.application.use_cases.criar_equipe import CriarEquipe
from app.application.use_cases.listar_equipes import ListarEquipes
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.exceptions.autenticacao import UsuarioNaoEncontradoError
from app.domain.exceptions.equipes import (
    EquipeInativaError,
    EquipeNaoEncontradaError,
)


router = APIRouter(prefix="/equipes", tags=["Equipes"])
administrador_required = exigir_perfil(PerfilAcesso.ADMINISTRADOR)


@router.post(
    "",
    response_model=EquipeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar equipe",
)
def criar_equipe(
    dados: CriarEquipeRequest,
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[CriarEquipe, Depends(get_criar_equipe)],
) -> EquipeResponse:
    equipe = caso_de_uso.executar(dados.nome)
    return EquipeResponse.model_validate(equipe)


@router.get(
    "",
    response_model=ListaEquipesResponse,
    summary="Listar equipes",
)
def listar_equipes(
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[ListarEquipes, Depends(get_listar_equipes)],
    pagina: Annotated[int, Query(ge=1)] = 1,
    itens_por_pagina: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ListaEquipesResponse:
    resultado = caso_de_uso.executar(pagina, itens_por_pagina)
    return ListaEquipesResponse(
        equipes=[
            EquipeResponse.model_validate(equipe)
            for equipe in resultado.equipes
        ],
        pagina=resultado.pagina,
        itens_por_pagina=resultado.itens_por_pagina,
        total=resultado.total,
        total_paginas=ceil(resultado.total / resultado.itens_por_pagina),
    )


@router.put(
    "/{equipe_id}/membros/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Associar usuário a uma equipe",
)
def associar_usuario_equipe(
    equipe_id: UUID,
    usuario_id: UUID,
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[
        AssociarUsuarioEquipe,
        Depends(get_associar_usuario_equipe),
    ],
) -> UsuarioResponse:
    try:
        usuario = caso_de_uso.executar(equipe_id, usuario_id)
    except EquipeNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipe não encontrada.",
        ) from erro
    except UsuarioNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        ) from erro
    except EquipeInativaError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível associar usuários a uma equipe inativa.",
        ) from erro
    return UsuarioResponse.model_validate(usuario)
