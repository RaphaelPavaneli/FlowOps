from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest

from app.application.services.executor_automacao import (
    ExecutorAutomacao,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_CONTROLADA,
    MENSAGEM_FALHA_INESPERADA,
)
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.domain.entities.automacao import Automacao
from app.domain.entities.equipe import Equipe
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.enums.resultado_teste_controlado import (
    ResultadoTesteControlado,
)
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao
from app.domain.exceptions.automacoes import (
    AutomacaoIndisponivelParaExecucaoError,
    AutomacaoNaoEncontradaError,
)
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.domain.value_objects.configuracao_teste_controlado import (
    ConfiguracaoTesteControlado,
)


MOMENTO_BASE = datetime(2026, 9, 30, 12, tzinfo=timezone.utc)
EQUIPE_ID = UUID("00000000-0000-0000-0000-000000000001")
USUARIO_ID = UUID("00000000-0000-0000-0000-000000000002")
AUTOMACAO_ID = UUID("00000000-0000-0000-0000-000000000003")


def criar_usuario() -> Usuario:
    return Usuario(
        id=USUARIO_ID,
        nome="Usuário executor",
        email="executor@email.com",
        senha_hash="hash-seguro",
        perfil_acesso=PerfilAcesso.USUARIO,
        equipe_id=EQUIPE_ID,
        ativo=True,
        criado_em=MOMENTO_BASE,
        atualizado_em=MOMENTO_BASE,
    )


def criar_equipe() -> Equipe:
    return Equipe(
        id=EQUIPE_ID,
        nome="Equipe Operações",
        ativa=True,
        criada_em=MOMENTO_BASE,
        atualizada_em=MOMENTO_BASE,
    )


def criar_automacao(
    status: StatusAutomacao = StatusAutomacao.ATIVA,
) -> Automacao:
    return Automacao(
        id=AUTOMACAO_ID,
        equipe_id=EQUIPE_ID,
        criada_por_usuario_id=USUARIO_ID,
        nome="Automação de teste",
        nome_normalizado="automação de teste",
        descricao=None,
        tipo_acao=TipoAcaoAutomacao.TESTE_CONTROLADO,
        configuracao_acao=ConfiguracaoTesteControlado(
            resultado=ResultadoTesteControlado.SUCESSO,
        ),
        status=status,
        criada_em=MOMENTO_BASE,
        atualizada_em=MOMENTO_BASE,
    )


def preparar_caso_de_uso(
    *,
    status_automacao: StatusAutomacao = StatusAutomacao.ATIVA,
) -> tuple[
    IniciarExecucao,
    Usuario,
    Automacao,
    Mock,
    Mock,
    Mock,
    list[StatusExecucao],
]:
    usuario = criar_usuario()
    equipe = criar_equipe()
    automacao = criar_automacao(status_automacao)

    automacao_repository = Mock(spec=AutomacaoRepository)
    equipe_repository = Mock(spec=EquipeRepository)
    execucao_repository = Mock(spec=ExecucaoRepository)
    executor = Mock(spec=ExecutorAutomacao)

    equipe_repository.buscar_por_id.return_value = equipe
    automacao_repository.buscar_por_id_e_equipe.return_value = automacao

    status_persistidos: list[StatusExecucao] = []

    def registrar_status(execucao: Execucao) -> Execucao:
        status_persistidos.append(execucao.status)
        return execucao

    execucao_repository.salvar.side_effect = registrar_status
    execucao_repository.atualizar.side_effect = registrar_status

    caso_de_uso = IniciarExecucao(
        automacao_repository=automacao_repository,
        equipe_repository=equipe_repository,
        execucao_repository=execucao_repository,
        executor_automacao=executor,
    )

    return (
        caso_de_uso,
        usuario,
        automacao,
        automacao_repository,
        execucao_repository,
        executor,
        status_persistidos,
    )


def test_execucao_com_sucesso_persiste_todas_as_transicoes() -> None:
    (
        caso_de_uso,
        usuario,
        automacao,
        _,
        execucao_repository,
        executor,
        status_persistidos,
    ) = preparar_caso_de_uso()

    resultado = caso_de_uso.executar(usuario, automacao.id)

    assert status_persistidos == [
        StatusExecucao.PENDENTE,
        StatusExecucao.PROCESSANDO,
        StatusExecucao.CONCLUIDA,
    ]
    assert resultado.status is StatusExecucao.CONCLUIDA
    assert resultado.mensagem_erro is None
    assert resultado.iniciada_em is not None
    assert resultado.finalizada_em is not None
    assert resultado.criada_em <= resultado.iniciada_em
    assert resultado.iniciada_em <= resultado.finalizada_em

    executor.executar.assert_called_once_with(automacao)
    execucao_repository.salvar.assert_called_once()
    assert execucao_repository.atualizar.call_count == 2


def test_falha_controlada_persiste_mensagem_segura() -> None:
    (
        caso_de_uso,
        usuario,
        automacao,
        _,
        execucao_repository,
        executor,
        status_persistidos,
    ) = preparar_caso_de_uso()

    executor.executar.side_effect = FalhaControladaAutomacaoError(
        MENSAGEM_FALHA_CONTROLADA
    )

    resultado = caso_de_uso.executar(usuario, automacao.id)

    assert status_persistidos == [
        StatusExecucao.PENDENTE,
        StatusExecucao.PROCESSANDO,
        StatusExecucao.FALHOU,
    ]
    assert resultado.status is StatusExecucao.FALHOU
    assert resultado.mensagem_erro == MENSAGEM_FALHA_CONTROLADA
    assert resultado.iniciada_em is not None
    assert resultado.finalizada_em is not None

    executor.executar.assert_called_once_with(automacao)
    execucao_repository.salvar.assert_called_once()
    assert execucao_repository.atualizar.call_count == 2


def test_falha_inesperada_nao_expoe_detalhe_sensivel() -> None:
    (
        caso_de_uso,
        usuario,
        automacao,
        _,
        execucao_repository,
        executor,
        status_persistidos,
    ) = preparar_caso_de_uso()

    executor.executar.side_effect = RuntimeError(
        "senha interna extremamente sensível"
    )

    resultado = caso_de_uso.executar(usuario, automacao.id)

    assert status_persistidos == [
        StatusExecucao.PENDENTE,
        StatusExecucao.PROCESSANDO,
        StatusExecucao.FALHOU,
    ]
    assert resultado.status is StatusExecucao.FALHOU
    assert resultado.mensagem_erro == MENSAGEM_FALHA_INESPERADA
    assert "senha interna" not in resultado.mensagem_erro
    assert resultado.iniciada_em is not None
    assert resultado.finalizada_em is not None

    executor.executar.assert_called_once_with(automacao)
    execucao_repository.salvar.assert_called_once()
    assert execucao_repository.atualizar.call_count == 2


@pytest.mark.parametrize(
    "status",
    [
        StatusAutomacao.RASCUNHO,
        StatusAutomacao.PAUSADA,
    ],
)
def test_automacao_inativa_nao_cria_execucao(
    status: StatusAutomacao,
) -> None:
    (
        caso_de_uso,
        usuario,
        automacao,
        _,
        execucao_repository,
        executor,
        status_persistidos,
    ) = preparar_caso_de_uso(status_automacao=status)

    with pytest.raises(AutomacaoIndisponivelParaExecucaoError):
        caso_de_uso.executar(usuario, automacao.id)

    assert status_persistidos == []
    execucao_repository.salvar.assert_not_called()
    execucao_repository.atualizar.assert_not_called()
    executor.executar.assert_not_called()


def test_automacao_inexistente_ou_de_outra_equipe_nao_cria_execucao() -> None:
    (
        caso_de_uso,
        usuario,
        _,
        automacao_repository,
        execucao_repository,
        executor,
        status_persistidos,
    ) = preparar_caso_de_uso()

    automacao_repository.buscar_por_id_e_equipe.return_value = None
    automacao_id = uuid4()

    with pytest.raises(AutomacaoNaoEncontradaError):
        caso_de_uso.executar(usuario, automacao_id)

    automacao_repository.buscar_por_id_e_equipe.assert_called_once_with(
        automacao_id,
        EQUIPE_ID,
    )
    assert status_persistidos == []
    execucao_repository.salvar.assert_not_called()
    execucao_repository.atualizar.assert_not_called()
    executor.executar.assert_not_called()