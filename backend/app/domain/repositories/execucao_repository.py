from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.execucao import Execucao


class ExecucaoRepository(ABC):
    """Contrato de persistência das execuções de automação."""

    @abstractmethod
    def salvar(self, execucao: Execucao) -> Execucao:
        """Persiste uma nova execução."""

    @abstractmethod
    def atualizar(self, execucao: Execucao) -> Execucao | None:
        """Atualiza uma execução existente."""

    @abstractmethod
    def buscar_por_id_e_equipe(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
    ) -> Execucao | None:
        """Busca uma execução somente dentro da equipe informada."""

    @abstractmethod
    def listar_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
        offset: int,
        limite: int,
    ) -> list[Execucao]:
        """Lista o histórico de uma automação dentro da equipe."""

    @abstractmethod
    def contar_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
    ) -> int:
        """Conta as execuções de uma automação dentro da equipe."""
