from app.application.services.executor_automacao import (
    ExecutorAutomacao,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_CONTROLADA,
)
from app.domain.entities.automacao import Automacao
from app.domain.enums.resultado_teste_controlado import (
    ResultadoTesteControlado,
)
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao


class ExecutorTesteControlado(ExecutorAutomacao):
    """Executa o cenário determinístico usado para validar o MVP."""

    def executar(self, automacao: Automacao) -> None:
        if automacao.tipo_acao is not TipoAcaoAutomacao.TESTE_CONTROLADO:
            raise ValueError("Tipo de ação não suportado pelo executor.")

        if (
            automacao.configuracao_acao.resultado
            is ResultadoTesteControlado.FALHA
        ):
            raise FalhaControladaAutomacaoError(
                MENSAGEM_FALHA_CONTROLADA
            )
