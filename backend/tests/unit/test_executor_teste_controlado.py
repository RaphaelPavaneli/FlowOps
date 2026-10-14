from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import subprocess
import sys
from time import sleep
from uuid import uuid4

import pytest

from app.application.services.executor_automacao import (
    ExecucaoCanceladaError,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_CONTROLADA,
)
from app.domain.entities.automacao import Automacao
from app.domain.enums.resultado_teste_controlado import ResultadoTesteControlado
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao
from app.domain.value_objects.configuracao_teste_controlado import ConfiguracaoTesteControlado
from app.infrastructure.executors.executor_teste_controlado import ExecutorTesteControlado


def criar_automacao(resultado: ResultadoTesteControlado) -> Automacao:
    agora = datetime(2026, 9, 29, 12, tzinfo=timezone.utc)
    return Automacao(
        id=uuid4(),
        equipe_id=uuid4(),
        criada_por_usuario_id=uuid4(),
        nome="Automação teste",
        nome_normalizado="automação teste",
        descricao=None,
        tipo_acao=TipoAcaoAutomacao.TESTE_CONTROLADO,
        configuracao_acao=ConfiguracaoTesteControlado(resultado=resultado),
        status=StatusAutomacao.ATIVA,
        criada_em=agora,
        atualizada_em=agora,
    )


def executar_cenario(resultado: ResultadoTesteControlado) -> None:
    execucao_id = uuid4()
    executor = ExecutorTesteControlado(duracao_segundos=0.01)
    executor.preparar(execucao_id)
    try:
        executor.executar(execucao_id, criar_automacao(resultado))
    finally:
        executor.liberar(execucao_id)


def test_executor_controlado_conclui_cenario_de_sucesso() -> None:
    executar_cenario(ResultadoTesteControlado.SUCESSO)


def test_executor_controlado_informa_falha_segura() -> None:
    with pytest.raises(
        FalhaControladaAutomacaoError,
        match=MENSAGEM_FALHA_CONTROLADA,
    ):
        executar_cenario(ResultadoTesteControlado.FALHA)


def test_script_de_falha_encerra_com_codigo_controlado() -> None:
    resultado = subprocess.run(
        [
            sys.executable,
            "-m",
            "app.infrastructure.executors.script_teste_controlado",
            "--duracao-segundos",
            "0",
            "--resultado",
            ResultadoTesteControlado.FALHA.value,
        ],
        check=False,
        timeout=2,
    )

    assert resultado.returncode == 2


def test_cancelamento_antes_do_inicio_impede_subprocesso() -> None:
    execucao_id = uuid4()
    executor = ExecutorTesteControlado(duracao_segundos=0.01)
    executor.preparar(execucao_id)

    assert executor.cancelar(execucao_id) is True
    with pytest.raises(ExecucaoCanceladaError):
        executor.executar(
            execucao_id,
            criar_automacao(ResultadoTesteControlado.SUCESSO),
        )
    executor.liberar(execucao_id)


def test_cancelamento_desconhecido_nao_afeta_outras_execucoes() -> None:
    executor = ExecutorTesteControlado(duracao_segundos=0.01)

    assert executor.cancelar(uuid4()) is False


def test_cancelamento_durante_execucao_encerra_subprocesso() -> None:
    execucao_id = uuid4()
    executor = ExecutorTesteControlado(duracao_segundos=5)
    executor.preparar(execucao_id)

    with ThreadPoolExecutor(max_workers=1) as pool:
        futuro = pool.submit(
            executor.executar,
            execucao_id,
            criar_automacao(ResultadoTesteControlado.SUCESSO),
        )
        sleep(0.1)
        assert executor.cancelar(execucao_id) is True
        with pytest.raises(ExecucaoCanceladaError):
            futuro.result(timeout=2)

    executor.liberar(execucao_id)


def test_execucoes_concorrentes_mantem_resultados_independentes() -> None:
    executor = ExecutorTesteControlado(duracao_segundos=0.05)
    sucesso_id = uuid4()
    falha_id = uuid4()
    executor.preparar(sucesso_id)
    executor.preparar(falha_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        sucesso = pool.submit(
            executor.executar,
            sucesso_id,
            criar_automacao(ResultadoTesteControlado.SUCESSO),
        )
        falha = pool.submit(
            executor.executar,
            falha_id,
            criar_automacao(ResultadoTesteControlado.FALHA),
        )
        assert sucesso.result(timeout=2) is None
        with pytest.raises(FalhaControladaAutomacaoError):
            falha.result(timeout=2)

    executor.liberar(sucesso_id)
    executor.liberar(falha_id)


def test_cancelar_uma_execucao_nao_interrompe_a_outra() -> None:
    executor = ExecutorTesteControlado(duracao_segundos=0.25)
    cancelada_id = uuid4()
    sucesso_id = uuid4()
    executor.preparar(cancelada_id)
    executor.preparar(sucesso_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        cancelada = pool.submit(
            executor.executar,
            cancelada_id,
            criar_automacao(ResultadoTesteControlado.SUCESSO),
        )
        sucesso = pool.submit(
            executor.executar,
            sucesso_id,
            criar_automacao(ResultadoTesteControlado.SUCESSO),
        )
        sleep(0.1)
        assert executor.cancelar(cancelada_id) is True
        with pytest.raises(ExecucaoCanceladaError):
            cancelada.result(timeout=2)
        assert sucesso.result(timeout=2) is None

    executor.liberar(cancelada_id)
    executor.liberar(sucesso_id)
