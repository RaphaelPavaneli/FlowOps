from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest

from app.application.services.despachante_execucao import DespachanteExecucao
from app.application.use_cases.iniciar_execucao import IniciarExecucao
from app.domain.entities.automacao import Automacao
from app.domain.entities.equipe import Equipe
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.enums.resultado_teste_controlado import ResultadoTesteControlado
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao
from app.domain.exceptions.automacoes import (
    AutomacaoIndisponivelParaExecucaoError,
    AutomacaoNaoEncontradaError,
)
from app.domain.exceptions.execucoes import (
    ExecucaoEmAndamentoError,
    FalhaAoAgendarExecucaoError,
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
    *, status_automacao: StatusAutomacao = StatusAutomacao.ATIVA
) -> tuple[IniciarExecucao, Usuario, Automacao, Mock, Mock, Mock]:
    usuario = criar_usuario()
    equipe = criar_equipe()
    automacao = criar_automacao(status_automacao)
    automacao_repository = Mock(spec=AutomacaoRepository)
    equipe_repository = Mock(spec=EquipeRepository)
    execucao_repository = Mock(spec=ExecucaoRepository)
    despachante = Mock(spec=DespachanteExecucao)
    equipe_repository.buscar_por_id.return_value = equipe
    automacao_repository.buscar_por_id_e_equipe.return_value = automacao
    execucao_repository.existe_ativa_por_automacao_e_equipe.return_value = False
    execucao_repository.salvar.side_effect = lambda execucao: execucao
    execucao_repository.atualizar_se_status.side_effect = lambda execucao, _: execucao

    return (
        IniciarExecucao(
            automacao_repository=automacao_repository,
            equipe_repository=equipe_repository,
            execucao_repository=execucao_repository,
            despachante_execucao=despachante,
        ),
        usuario,
        automacao,
        automacao_repository,
        execucao_repository,
        despachante,
    )


def test_iniciar_persiste_pendente_e_despacha_sem_aguardar_resultado() -> None:
    caso, usuario, automacao, _, repositorio, despachante = preparar_caso_de_uso()

    resultado = caso.executar(usuario, automacao.id)

    assert resultado.status is StatusExecucao.PENDENTE
    assert resultado.iniciada_em is None
    assert resultado.finalizada_em is None
    repositorio.salvar.assert_called_once_with(resultado)
    despachante.despachar.assert_called_once_with(resultado.id, EQUIPE_ID, automacao)


def test_execucao_ativa_da_mesma_automacao_e_bloqueada() -> None:
    caso, usuario, automacao, _, repositorio, despachante = preparar_caso_de_uso()
    repositorio.existe_ativa_por_automacao_e_equipe.return_value = True

    with pytest.raises(ExecucaoEmAndamentoError):
        caso.executar(usuario, automacao.id)

    repositorio.salvar.assert_not_called()
    despachante.despachar.assert_not_called()


def test_falha_ao_despachar_finaliza_registro_e_retorna_erro_de_agendamento() -> None:
    caso, usuario, automacao, _, repositorio, despachante = preparar_caso_de_uso()
    despachante.despachar.side_effect = RuntimeError("fila indisponível")

    with pytest.raises(FalhaAoAgendarExecucaoError):
        caso.executar(usuario, automacao.id)

    execucao_falha, status_esperados = repositorio.atualizar_se_status.call_args.args
    assert execucao_falha.status is StatusExecucao.FALHOU
    assert execucao_falha.finalizada_em is not None
    assert status_esperados == frozenset({StatusExecucao.PENDENTE})


@pytest.mark.parametrize("status", [StatusAutomacao.RASCUNHO, StatusAutomacao.PAUSADA])
def test_automacao_inativa_nao_cria_execucao(status: StatusAutomacao) -> None:
    caso, usuario, automacao, _, repositorio, despachante = preparar_caso_de_uso(
        status_automacao=status
    )

    with pytest.raises(AutomacaoIndisponivelParaExecucaoError):
        caso.executar(usuario, automacao.id)

    repositorio.salvar.assert_not_called()
    despachante.despachar.assert_not_called()


def test_automacao_inexistente_ou_de_outra_equipe_nao_cria_execucao() -> None:
    caso, usuario, _, automacao_repository, repositorio, despachante = preparar_caso_de_uso()
    automacao_repository.buscar_por_id_e_equipe.return_value = None
    automacao_id = uuid4()

    with pytest.raises(AutomacaoNaoEncontradaError):
        caso.executar(usuario, automacao_id)

    automacao_repository.buscar_por_id_e_equipe.assert_called_once_with(
        automacao_id, EQUIPE_ID
    )
    repositorio.salvar.assert_not_called()
    despachante.despachar.assert_not_called()
