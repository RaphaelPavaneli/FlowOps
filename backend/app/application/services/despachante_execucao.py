from typing import Protocol
from uuid import UUID

from app.domain.entities.automacao import Automacao


class DespachanteExecucao(Protocol):
    """Contrato para processar execuções fora da requisição HTTP."""

    def despachar(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
        automacao: Automacao,
    ) -> None:
        """Agenda uma execução para processamento em segundo plano."""

    def cancelar(self, execucao_id: UUID) -> bool:
        """Solicita o cancelamento da execução informada."""

    def encerrar(self) -> None:
        """Libera os recursos locais durante o desligamento da aplicação."""
