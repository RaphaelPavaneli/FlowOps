from typing import Protocol

from app.domain.entities.automacao import Automacao


MENSAGEM_FALHA_CONTROLADA = (
    "A automação de teste foi configurada para simular uma falha."
)
MENSAGEM_FALHA_INESPERADA = (
    "Não foi possível concluir a execução da automação."
)


class FalhaControladaAutomacaoError(Exception):
    """Representa uma falha esperada e segura da ação executada."""


class ExecutorAutomacao(Protocol):
    """Contrato mínimo para executar a ação configurada na automação."""

    def executar(self, automacao: Automacao) -> None:
        """Executa a ação ou informa uma falha controlada."""
