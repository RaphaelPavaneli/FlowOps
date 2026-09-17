from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.autenticacao import get_usuario_atual
from app.api.dependencies.execucoes import get_iniciar_execucao
from app.api.schemas.execucoes import (
    ExecucaoResponse,
    IniciarExecucaoRequest,
)
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.automacoes import (
    AutomacaoIndisponivelParaExecucaoError,
    AutomacaoNaoEncontradaError,
    EquipeUsuarioIndisponivelError,
    UsuarioSemEquipeError,
)


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
