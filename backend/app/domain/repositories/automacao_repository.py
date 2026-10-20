from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.automacao import Automacao
from app.domain.enums.status_automacao import StatusAutomacao


class AutomacaoRepository(ABC):
    """Contrato de persistência das automações."""

    @abstractmethod
    def buscar_por_nome_normalizado(
        self,
        equipe_id: UUID,
        nome_normalizado: str,
    ) -> Automacao | None:
        """Busca uma automação pelo nome único dentro da equipe."""

    @abstractmethod
    def buscar_por_id_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
    ) -> Automacao | None:
        """Busca uma automação somente dentro da equipe informada."""

    @abstractmethod
    def listar_por_equipe(
        self,
        equipe_id: UUID,
        offset: int,
        limite: int,
        busca_nome_normalizado: str | None = None,
        status: frozenset[StatusAutomacao] = frozenset(),
    ) -> list[Automacao]:
        """Lista somente as automações da equipe informada."""

    @abstractmethod
    def contar_filtradas_por_equipe(
        self,
        equipe_id: UUID,
        busca_nome_normalizado: str | None = None,
        status: frozenset[StatusAutomacao] = frozenset(),
    ) -> int:
        """Conta as automações da equipe que atendem aos filtros."""

    @abstractmethod
    def contar_por_status_e_equipe(
        self,
        equipe_id: UUID,
    ) -> dict[StatusAutomacao, int]:
        """Conta as automações da equipe agrupadas por status."""

    @abstractmethod
    def salvar(self, automacao: Automacao) -> Automacao:
        """Persiste uma nova automação."""

    @abstractmethod
    def atualizar(self, automacao: Automacao) -> Automacao | None:
        """Atualiza uma automação somente dentro da equipe informada."""
