from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.domain.entities.automacao import Automacao
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.exceptions.automacoes import (
    AutomacaoIndisponivelParaExecucaoError,
    TransicaoStatusAutomacaoInvalidaError,
)


MOMENTO_CRIACAO = datetime(2026, 9, 17, 12, tzinfo=timezone.utc)
MOMENTO_ALTERACAO = MOMENTO_CRIACAO + timedelta(minutes=1)


def criar_automacao(
    status: StatusAutomacao = StatusAutomacao.RASCUNHO,
) -> Automacao:
    return Automacao(
        id=uuid4(),
        equipe_id=uuid4(),
        criada_por_usuario_id=uuid4(),
        nome="Automação teste",
        nome_normalizado="automação teste",
        descricao=None,
        status=status,
        criada_em=MOMENTO_CRIACAO,
        atualizada_em=MOMENTO_CRIACAO,
    )


@pytest.mark.parametrize(
    "status_inicial",
    [StatusAutomacao.RASCUNHO, StatusAutomacao.PAUSADA],
)
def test_automacao_em_rascunho_ou_pausada_pode_ser_ativada(
    status_inicial: StatusAutomacao,
) -> None:
    automacao = criar_automacao(status_inicial)

    automacao.ativar(MOMENTO_ALTERACAO)

    assert automacao.status is StatusAutomacao.ATIVA
    assert automacao.atualizada_em == MOMENTO_ALTERACAO


def test_automacao_ativa_pode_ser_pausada() -> None:
    automacao = criar_automacao(StatusAutomacao.ATIVA)

    automacao.pausar(MOMENTO_ALTERACAO)

    assert automacao.status is StatusAutomacao.PAUSADA
    assert automacao.atualizada_em == MOMENTO_ALTERACAO


@pytest.mark.parametrize(
    ("status_inicial", "operacao"),
    [
        (StatusAutomacao.ATIVA, "ativar"),
        (StatusAutomacao.RASCUNHO, "pausar"),
        (StatusAutomacao.PAUSADA, "pausar"),
    ],
)
def test_transicao_invalida_preserva_status_e_data(
    status_inicial: StatusAutomacao,
    operacao: str,
) -> None:
    automacao = criar_automacao(status_inicial)

    with pytest.raises(TransicaoStatusAutomacaoInvalidaError):
        getattr(automacao, operacao)(MOMENTO_ALTERACAO)

    assert automacao.status is status_inicial
    assert automacao.atualizada_em == MOMENTO_CRIACAO


def test_automacao_ativa_esta_disponivel_para_execucao() -> None:
    automacao = criar_automacao(StatusAutomacao.ATIVA)

    automacao.garantir_disponivel_para_execucao()


@pytest.mark.parametrize(
    "status",
    [StatusAutomacao.RASCUNHO, StatusAutomacao.PAUSADA],
)
def test_automacao_nao_ativa_impede_nova_execucao(
    status: StatusAutomacao,
) -> None:
    automacao = criar_automacao(status)

    with pytest.raises(AutomacaoIndisponivelParaExecucaoError):
        automacao.garantir_disponivel_para_execucao()
