from math import ceil
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.autenticacao import get_usuario_atual
from app.api.dependencies.automacoes import (
    get_alterar_status_automacao,
    get_criar_automacao,
    get_listar_automacoes,
)
from app.api.schemas.automacoes import (
    AutomacaoResponse,
    CriarAutomacaoRequest,
    ListaAutomacoesResponse,
)
from app.application.use_cases.alterar_status_automacao import (
    AlterarStatusAutomacao,
)
from app.application.use_cases.criar_automacao import CriarAutomacao
from app.application.use_cases.listar_automacoes import ListarAutomacoes
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.automacoes import (
    AutomacaoNaoEncontradaError,
    AutomacaoNomeDuplicadoError,
    EquipeUsuarioIndisponivelError,
    TransicaoStatusAutomacaoInvalidaError,
    UsuarioSemEquipeError,
)


router = APIRouter(prefix="/automacoes", tags=["Automações"])


@router.post(
    "",
    response_model=AutomacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar automação",
)
def criar_automacao(
    dados: CriarAutomacaoRequest,
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[CriarAutomacao, Depends(get_criar_automacao)],
) -> AutomacaoResponse:
    try:
        automacao = caso_de_uso.executar(
            usuario,
            dados.nome,
            dados.descricao,
        )
    except AutomacaoNomeDuplicadoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma automação com este nome na equipe.",
        ) from erro
    except (UsuarioSemEquipeError, EquipeUsuarioIndisponivelError) as erro:
        raise _erro_contexto_equipe(erro) from erro
    return AutomacaoResponse.model_validate(automacao)


@router.get(
    "",
    response_model=ListaAutomacoesResponse,
    summary="Listar automações da equipe",
)
def listar_automacoes(
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[
        ListarAutomacoes,
        Depends(get_listar_automacoes),
    ],
    pagina: Annotated[int, Query(ge=1)] = 1,
    itens_por_pagina: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ListaAutomacoesResponse:
    try:
        resultado = caso_de_uso.executar(
            usuario,
            pagina,
            itens_por_pagina,
        )
    except (UsuarioSemEquipeError, EquipeUsuarioIndisponivelError) as erro:
        raise _erro_contexto_equipe(erro) from erro
    return ListaAutomacoesResponse(
        automacoes=[
            AutomacaoResponse.model_validate(automacao)
            for automacao in resultado.automacoes
        ],
        pagina=resultado.pagina,
        itens_por_pagina=resultado.itens_por_pagina,
        total=resultado.total,
        total_paginas=ceil(resultado.total / resultado.itens_por_pagina),
    )


@router.post(
    "/{automacao_id}/ativar",
    response_model=AutomacaoResponse,
    summary="Ativar automação",
)
def ativar_automacao(
    automacao_id: UUID,
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[
        AlterarStatusAutomacao,
        Depends(get_alterar_status_automacao),
    ],
) -> AutomacaoResponse:
    try:
        automacao = caso_de_uso.ativar(usuario, automacao_id)
    except AutomacaoNaoEncontradaError as erro:
        raise _automacao_nao_encontrada() from erro
    except TransicaoStatusAutomacaoInvalidaError as erro:
        raise _transicao_status_invalida(erro) from erro
    except (UsuarioSemEquipeError, EquipeUsuarioIndisponivelError) as erro:
        raise _erro_contexto_equipe(erro) from erro
    return AutomacaoResponse.model_validate(automacao)


@router.post(
    "/{automacao_id}/pausar",
    response_model=AutomacaoResponse,
    summary="Pausar automação",
)
def pausar_automacao(
    automacao_id: UUID,
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[
        AlterarStatusAutomacao,
        Depends(get_alterar_status_automacao),
    ],
) -> AutomacaoResponse:
    try:
        automacao = caso_de_uso.pausar(usuario, automacao_id)
    except AutomacaoNaoEncontradaError as erro:
        raise _automacao_nao_encontrada() from erro
    except TransicaoStatusAutomacaoInvalidaError as erro:
        raise _transicao_status_invalida(erro) from erro
    except (UsuarioSemEquipeError, EquipeUsuarioIndisponivelError) as erro:
        raise _erro_contexto_equipe(erro) from erro
    return AutomacaoResponse.model_validate(automacao)


def _automacao_nao_encontrada() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Automação não encontrada.",
    )


def _transicao_status_invalida(
    erro: TransicaoStatusAutomacaoInvalidaError,
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(erro),
    )


def _erro_contexto_equipe(
    erro: UsuarioSemEquipeError | EquipeUsuarioIndisponivelError,
) -> HTTPException:
    if isinstance(erro, UsuarioSemEquipeError):
        detalhe = "O usuário precisa estar associado a uma equipe."
    else:
        detalhe = "A equipe do usuário não está disponível."
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detalhe,
    )
