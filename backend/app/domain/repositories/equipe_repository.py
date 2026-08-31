from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.equipe import Equipe


class EquipeRepository(ABC):
    """Contrato de persistência de equipes."""

    @abstractmethod
    def buscar_por_id(self, equipe_id: UUID) -> Equipe | None:
        """Busca uma equipe pelo identificador."""

    @abstractmethod
    def listar(self, offset: int, limite: int) -> list[Equipe]:
        """Lista equipes de forma paginada."""

    @abstractmethod
    def contar(self) -> int:
        """Retorna a quantidade total de equipes."""

    @abstractmethod
    def salvar(self, equipe: Equipe) -> Equipe:
        """Persiste uma nova equipe."""
