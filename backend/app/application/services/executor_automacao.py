from typing import Protocol
from uuid import UUID

from app.domain.entities.automacao import Automacao


MENSAGEM_FALHA_CONTROLADA = (
    "A automação de teste foi configurada para simular uma falha."
)
MENSAGEM_FALHA_INESPERADA = (
    "Não foi possível concluir a execução da automação."
)
MENSAGEM_EXECUCAO_INTERROMPIDA = (
    "A execução foi interrompida porque o serviço foi reiniciado."
)


class FalhaControladaAutomacaoError(Exception):
    """Representa uma falha esperada e segura da ação executada."""


class ExecucaoCanceladaError(Exception):
    """Informa ao processador que o cancelamento já foi persistido."""


class ExecutorAutomacao(Protocol):
    """Contrato mínimo para executar a ação configurada na automação."""

    def preparar(self, execucao_id: UUID) -> None:
        """Registra a execução antes de enviá-la ao processamento."""

    def executar(self, execucao_id: UUID, automacao: Automacao) -> None:
        """Executa a ação ou informa uma falha controlada."""

    def cancelar(self, execucao_id: UUID) -> bool:
        """Interrompe somente o processo relacionado à execução."""

    def liberar(self, execucao_id: UUID) -> None:
        """Remove os recursos mantidos para a execução."""

    def encerrar_todos(self) -> None:
        """Encerra processos locais durante o desligamento da aplicação."""
