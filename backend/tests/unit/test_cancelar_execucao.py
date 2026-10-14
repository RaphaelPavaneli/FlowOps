from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.application.services.despachante_execucao import DespachanteExecucao
from app.application.use_cases.cancelar_execucao import CancelarExecucao
from app.domain.entities.equipe import Equipe
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.execucoes import (
    ExecucaoIndisponivelParaCancelamentoError,
    ExecucaoNaoEncontradaError,
)
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


AGORA = datetime(2026, 10, 2, 12, tzinfo=timezone.utc)


def preparar(status: StatusExecucao) -> tuple[CancelarExecucao, Usuario, Execucao, Mock, Mock]:
    equipe_id = uuid4()
    usuario = Usuario(
        id=uuid4(),
        nome="Usuário",
        email="usuario@email.com",
        senha_hash="hash",
        perfil_acesso=PerfilAcesso.USUARIO,
        equipe_id=equipe_id,
        ativo=True,
        criado_em=AGORA,
        atualizado_em=AGORA,
    )
    equipe = Equipe(
        id=equipe_id,
        nome="Equipe",
        ativa=True,
        criada_em=AGORA,
        atualizada_em=AGORA,
    )
    execucao = Execucao(
        id=uuid4(),
        automacao_id=uuid4(),
        equipe_id=equipe_id,
        solicitada_por_usuario_id=usuario.id,
        status=status,
        mensagem_erro=None,
        criada_em=AGORA,
        iniciada_em=AGORA if status is not StatusExecucao.PENDENTE else None,
        finalizada_em=AGORA if status in {
            StatusExecucao.CONCLUIDA,
            StatusExecucao.FALHOU,
            StatusExecucao.CANCELADA,
        } else None,
        atualizada_em=AGORA,
    )
    equipe_repository = Mock(spec=EquipeRepository)
    execucao_repository = Mock(spec=ExecucaoRepository)
    despachante = Mock(spec=DespachanteExecucao)
    equipe_repository.buscar_por_id.return_value = equipe
    execucao_repository.buscar_por_id_e_equipe.return_value = execucao
    execucao_repository.atualizar_se_status.side_effect = lambda item, _: item
    return (
        CancelarExecucao(equipe_repository, execucao_repository, despachante),
        usuario,
        execucao,
        execucao_repository,
        despachante,
    )


@pytest.mark.parametrize("status", [StatusExecucao.PENDENTE, StatusExecucao.PROCESSANDO])
def test_cancela_execucao_ativa_e_sinaliza_processo(status: StatusExecucao) -> None:
    caso, usuario, execucao, repositorio, despachante = preparar(status)

    resultado = caso.executar(usuario, execucao.id)

    assert resultado.status is StatusExecucao.CANCELADA
    assert resultado.finalizada_em is not None
    repositorio.atualizar_se_status.assert_called_once()
    despachante.cancelar.assert_called_once_with(execucao.id)


@pytest.mark.parametrize(
    "status",
    [StatusExecucao.CONCLUIDA, StatusExecucao.FALHOU, StatusExecucao.CANCELADA],
)
def test_estado_terminal_nao_pode_ser_cancelado(status: StatusExecucao) -> None:
    caso, usuario, execucao, _, despachante = preparar(status)

    with pytest.raises(ExecucaoIndisponivelParaCancelamentoError):
        caso.executar(usuario, execucao.id)

    despachante.cancelar.assert_not_called()


def test_execucao_de_outra_equipe_e_tratada_como_inexistente() -> None:
    caso, usuario, execucao, repositorio, despachante = preparar(StatusExecucao.PENDENTE)
    repositorio.buscar_por_id_e_equipe.return_value = None

    with pytest.raises(ExecucaoNaoEncontradaError):
        caso.executar(usuario, execucao.id)

    despachante.cancelar.assert_not_called()


def test_concorrencia_que_finaliza_antes_do_cancelamento_retorna_conflito() -> None:
    caso, usuario, execucao, repositorio, despachante = preparar(StatusExecucao.PROCESSANDO)
    repositorio.atualizar_se_status.return_value = None
    repositorio.atualizar_se_status.side_effect = None

    with pytest.raises(ExecucaoIndisponivelParaCancelamentoError):
        caso.executar(usuario, execucao.id)

    despachante.cancelar.assert_not_called()
