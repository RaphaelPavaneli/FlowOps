from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

from app.application.services.executor_automacao import (
    ExecucaoCanceladaError,
    ExecutorAutomacao,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_CONTROLADA,
    MENSAGEM_FALHA_INESPERADA,
)
from app.application.use_cases.processar_execucao import ProcessarExecucao
from app.domain.entities.automacao import Automacao
from app.domain.entities.execucao import Execucao
from app.domain.enums.resultado_teste_controlado import ResultadoTesteControlado
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.domain.value_objects.configuracao_teste_controlado import ConfiguracaoTesteControlado


AGORA = datetime(2026, 10, 2, 12, tzinfo=timezone.utc)


def criar_automacao() -> Automacao:
    return Automacao(
        id=uuid4(),
        equipe_id=uuid4(),
        criada_por_usuario_id=uuid4(),
        nome="Automação",
        nome_normalizado="automação",
        descricao=None,
        tipo_acao=TipoAcaoAutomacao.TESTE_CONTROLADO,
        configuracao_acao=ConfiguracaoTesteControlado(
            resultado=ResultadoTesteControlado.SUCESSO
        ),
        status=StatusAutomacao.ATIVA,
        criada_em=AGORA,
        atualizada_em=AGORA,
    )


def criar_execucao(automacao: Automacao) -> Execucao:
    return Execucao(
        id=uuid4(),
        automacao_id=automacao.id,
        equipe_id=automacao.equipe_id,
        solicitada_por_usuario_id=uuid4(),
        status=StatusExecucao.PENDENTE,
        mensagem_erro=None,
        criada_em=AGORA,
        iniciada_em=None,
        finalizada_em=None,
        atualizada_em=AGORA,
    )


def preparar() -> tuple[ProcessarExecucao, Execucao, Automacao, Mock, Mock]:
    automacao = criar_automacao()
    execucao = criar_execucao(automacao)
    repositorio = Mock(spec=ExecucaoRepository)
    executor = Mock(spec=ExecutorAutomacao)
    repositorio.buscar_por_id_e_equipe.return_value = execucao
    repositorio.atualizar_se_status.side_effect = lambda atualizada, _: atualizada
    return (
        ProcessarExecucao(repositorio, executor),
        execucao,
        automacao,
        repositorio,
        executor,
    )


def test_processamento_conclui_e_libera_executor() -> None:
    caso, execucao, automacao, repositorio, executor = preparar()

    caso.executar(execucao.id, execucao.equipe_id, automacao)

    assert execucao.status is StatusExecucao.CONCLUIDA
    assert execucao.iniciada_em is not None
    assert execucao.finalizada_em is not None
    executor.executar.assert_called_once_with(execucao.id, automacao)
    executor.liberar.assert_called_once_with(execucao.id)
    assert repositorio.atualizar_se_status.call_count == 2


def test_falha_controlada_e_registrada_com_mensagem_segura() -> None:
    caso, execucao, automacao, repositorio, executor = preparar()
    executor.executar.side_effect = FalhaControladaAutomacaoError(
        MENSAGEM_FALHA_CONTROLADA
    )

    caso.executar(execucao.id, execucao.equipe_id, automacao)

    assert execucao.status is StatusExecucao.FALHOU
    assert execucao.mensagem_erro == MENSAGEM_FALHA_CONTROLADA
    assert repositorio.atualizar_se_status.call_count == 2


def test_falha_inesperada_nao_expoe_detalhes_internos() -> None:
    caso, execucao, automacao, _, executor = preparar()
    executor.executar.side_effect = RuntimeError("senha interna sensível")

    caso.executar(execucao.id, execucao.equipe_id, automacao)

    assert execucao.status is StatusExecucao.FALHOU
    assert execucao.mensagem_erro == MENSAGEM_FALHA_INESPERADA
    assert "senha" not in execucao.mensagem_erro


def test_cancelamento_nao_e_sobrescrito_pelo_worker() -> None:
    caso, execucao, automacao, repositorio, executor = preparar()
    executor.executar.side_effect = ExecucaoCanceladaError

    caso.executar(execucao.id, execucao.equipe_id, automacao)

    assert execucao.status is StatusExecucao.PROCESSANDO
    assert repositorio.atualizar_se_status.call_count == 1
    executor.liberar.assert_called_once_with(execucao.id)


def test_worker_nao_inicia_quando_estado_pendente_ja_foi_alterado() -> None:
    caso, execucao, automacao, repositorio, executor = preparar()
    repositorio.atualizar_se_status.return_value = None
    repositorio.atualizar_se_status.side_effect = None

    caso.executar(execucao.id, execucao.equipe_id, automacao)

    executor.executar.assert_not_called()
    executor.liberar.assert_called_once_with(execucao.id)
