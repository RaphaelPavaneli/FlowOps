from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.execucoes import (
    MensagemFalhaExecucaoObrigatoriaError,
    TransicaoStatusExecucaoInvalidaError,
)


MOMENTO_CRIACAO = datetime(2026, 9, 14, 12, tzinfo=timezone.utc)
MOMENTO_INICIO = MOMENTO_CRIACAO + timedelta(minutes=1)
MOMENTO_FINAL = MOMENTO_INICIO + timedelta(minutes=2)


def criar_execucao() -> Execucao:
    return Execucao(
        id=uuid4(),
        automacao_id=uuid4(),
        equipe_id=uuid4(),
        solicitada_por_usuario_id=uuid4(),
        status=StatusExecucao.PENDENTE,
        mensagem_erro=None,
        criada_em=MOMENTO_CRIACAO,
        iniciada_em=None,
        finalizada_em=None,
        atualizada_em=MOMENTO_CRIACAO,
    )


def test_execucao_pendente_pode_iniciar() -> None:
    execucao = criar_execucao()

    execucao.iniciar(MOMENTO_INICIO)

    assert execucao.status is StatusExecucao.PROCESSANDO
    assert execucao.iniciada_em == MOMENTO_INICIO
    assert execucao.finalizada_em is None
    assert execucao.atualizada_em == MOMENTO_INICIO


def test_execucao_processando_pode_concluir() -> None:
    execucao = criar_execucao()
    execucao.iniciar(MOMENTO_INICIO)

    execucao.concluir(MOMENTO_FINAL)

    assert execucao.status is StatusExecucao.CONCLUIDA
    assert execucao.mensagem_erro is None
    assert execucao.finalizada_em == MOMENTO_FINAL
    assert execucao.atualizada_em == MOMENTO_FINAL


@pytest.mark.parametrize(
    "iniciar_antes",
    [False, True],
)
def test_execucao_pendente_ou_processando_pode_falhar(
    iniciar_antes: bool,
) -> None:
    execucao = criar_execucao()
    if iniciar_antes:
        execucao.iniciar(MOMENTO_INICIO)

    execucao.falhar("Falha de processamento.", MOMENTO_FINAL)

    assert execucao.status is StatusExecucao.FALHOU
    assert execucao.mensagem_erro == "Falha de processamento."
    assert execucao.finalizada_em == MOMENTO_FINAL
    assert execucao.atualizada_em == MOMENTO_FINAL
    assert execucao.iniciada_em == (
        MOMENTO_INICIO if iniciar_antes else None
    )


def test_mensagem_de_falha_e_normalizada() -> None:
    execucao = criar_execucao()

    execucao.falhar("  Arquivo   inválido.\nTente novamente.  ", MOMENTO_FINAL)

    assert execucao.mensagem_erro == (
        "Arquivo inválido. Tente novamente."
    )


def test_falha_exige_mensagem() -> None:
    execucao = criar_execucao()

    with pytest.raises(MensagemFalhaExecucaoObrigatoriaError):
        execucao.falhar("   ", MOMENTO_FINAL)

    assert execucao.status is StatusExecucao.PENDENTE
    assert execucao.finalizada_em is None
    assert execucao.atualizada_em == MOMENTO_CRIACAO


def test_execucao_pendente_nao_pode_concluir() -> None:
    execucao = criar_execucao()

    with pytest.raises(TransicaoStatusExecucaoInvalidaError):
        execucao.concluir(MOMENTO_FINAL)


def test_execucao_processando_nao_pode_iniciar_novamente() -> None:
    execucao = criar_execucao()
    execucao.iniciar(MOMENTO_INICIO)

    with pytest.raises(TransicaoStatusExecucaoInvalidaError):
        execucao.iniciar(MOMENTO_FINAL)


def test_execucao_concluida_nao_pode_iniciar_novamente() -> None:
    execucao = criar_execucao()
    execucao.iniciar(MOMENTO_INICIO)
    execucao.concluir(MOMENTO_FINAL)

    with pytest.raises(TransicaoStatusExecucaoInvalidaError):
        execucao.iniciar(MOMENTO_FINAL)


def test_execucao_com_falha_nao_pode_concluir() -> None:
    execucao = criar_execucao()
    execucao.falhar("Falha", MOMENTO_FINAL)

    with pytest.raises(TransicaoStatusExecucaoInvalidaError):
        execucao.concluir(MOMENTO_FINAL)
