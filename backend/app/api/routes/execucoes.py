from math import ceil
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.autenticacao import get_usuario_atual
from app.api.dependencies.execucoes import (
    get_buscar_execucao,
    get_iniciar_execucao,
    get_listar_execucoes,
)
from app.api.schemas.execucoes import (
    ExecucaoResponse,
    IniciarExecucaoRequest,
    ListaExecucoesResponse,
)
from app.application.use_cases.buscar_execucao import BuscarExecucao
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.application.use_cases.listar_execucoes import ListarExecucoes
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.automacoes import (
    AutomacaoIndisponivelParaExecucaoError,
    AutomacaoNaoEncontradaError,
    EquipeUsuarioIndisponivelError,
    UsuarioSemEquipeError,
)
from app.domain.exceptions.execucoes import ExecucaoNaoEncontradaError


router = APIRouter(tags=["Execuções"])


@router.post(
    "/automacoes/{automacao_id}/execucoes",
    response_model=ExecucaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar execução manual",
)
def iniciar_execucao(
    automacao_id: UUID,
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[
        IniciarExecucao,
        Depends(get_iniciar_execucao),
    ],
    dados: IniciarExecucaoRequest | None = None,
) -> ExecucaoResponse:
    try:
        execucao = caso_de_uso.executar(usuario, automacao_id)
    except AutomacaoNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automação não encontrada.",
        ) from erro
    except AutomacaoIndisponivelParaExecucaoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A automação precisa estar ativa para ser executada.",
        ) from erro
    except UsuarioSemEquipeError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O usuário precisa estar associado a uma equipe.",
        ) from erro
    except EquipeUsuarioIndisponivelError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A equipe do usuário não está disponível.",
        ) from erro

    return ExecucaoResponse.model_validate(execucao)


@router.get(
    "/automacoes/{automacao_id}/execucoes",
    response_model=ListaExecucoesResponse,
    summary="Listar histórico de execuções",
)
def listar_execucoes(
    automacao_id: UUID,
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[
        ListarExecucoes,
        Depends(get_listar_execucoes),
    ],
    pagina: Annotated[int, Query(ge=1)] = 1,
    itens_por_pagina: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ListaExecucoesResponse:
    try:
        resultado = caso_de_uso.executar(
            usuario,
            automacao_id,
            pagina,
            itens_por_pagina,
        )
    except AutomacaoNaoEncontradaError as erro:
        raise _automacao_nao_encontrada() from erro
    except (UsuarioSemEquipeError, EquipeUsuarioIndisponivelError) as erro:
        raise _erro_contexto_equipe(erro) from erro

    return ListaExecucoesResponse(
        execucoes=[
            ExecucaoResponse.model_validate(execucao)
            for execucao in resultado.execucoes
        ],
        pagina=resultado.pagina,
        itens_por_pagina=resultado.itens_por_pagina,
        total=resultado.total,
        total_paginas=ceil(resultado.total / resultado.itens_por_pagina),
    )


@router.get(
    "/execucoes/{execucao_id}",
    response_model=ExecucaoResponse,
    summary="Consultar detalhes da execução",
)
def buscar_execucao(
    execucao_id: UUID,
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
    caso_de_uso: Annotated[
        BuscarExecucao,
        Depends(get_buscar_execucao),
    ],
) -> ExecucaoResponse:
    try:
        execucao = caso_de_uso.executar(usuario, execucao_id)
    except ExecucaoNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execução não encontrada.",
        ) from erro
    except (UsuarioSemEquipeError, EquipeUsuarioIndisponivelError) as erro:
        raise _erro_contexto_equipe(erro) from erro

    return ExecucaoResponse.model_validate(execucao)


def _automacao_nao_encontrada() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Automação não encontrada.",
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
