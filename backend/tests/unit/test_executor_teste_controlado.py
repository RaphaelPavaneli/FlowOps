from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.services.executor_automacao import (
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_CONTROLADA,
)
from app.domain.entities.automacao import Automacao
from app.domain.enums.resultado_teste_controlado import (
    ResultadoTesteControlado,
)
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao
from app.domain.value_objects.configuracao_teste_controlado import (
    ConfiguracaoTesteControlado,
)
from app.infrastructure.executors.executor_teste_controlado import (
    ExecutorTesteControlado,
)


def criar_automacao(
    resultado: ResultadoTesteControlado,
) -> Automacao:
    agora = datetime(2026, 9, 29, 12, tzinfo=timezone.utc)
    return Automacao(
        id=uuid4(),
        equipe_id=uuid4(),
        criada_por_usuario_id=uuid4(),
        nome="Automação teste",
        nome_normalizado="automação teste",
        descricao=None,
        tipo_acao=TipoAcaoAutomacao.TESTE_CONTROLADO,
        configuracao_acao=ConfiguracaoTesteControlado(
            resultado=resultado,
        ),
        status=StatusAutomacao.ATIVA,
        criada_em=agora,
        atualizada_em=agora,
    )


def test_executor_controlado_conclui_cenario_de_sucesso() -> None:
    automacao = criar_automacao(ResultadoTesteControlado.SUCESSO)

    ExecutorTesteControlado().executar(automacao)


def test_executor_controlado_informa_falha_segura() -> None:
    automacao = criar_automacao(ResultadoTesteControlado.FALHA)

    with pytest.raises(
        FalhaControladaAutomacaoError,
        match=MENSAGEM_FALHA_CONTROLADA,
    ):
        ExecutorTesteControlado().executar(automacao)
