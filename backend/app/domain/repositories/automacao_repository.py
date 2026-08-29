from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.automacao import Automacao


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
    def listar_por_equipe(
        self,
        equipe_id: UUID,
        offset: int,
        limite: int,
    ) -> list[Automacao]:
        """Lista somente as automações da equipe informada."""

    @abstractmethod
    def contar_por_equipe(self, equipe_id: UUID) -> int:
        """Conta somente as automações da equipe informada."""

    @abstractmethod
    def salvar(self, automacao: Automacao) -> Automacao:
        """Persiste uma nova automação."""
