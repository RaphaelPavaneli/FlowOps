from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.usuario import Usuario


class UsuarioRepository(ABC):
    """Contrato de persistência de usuários."""

    @abstractmethod
    def buscar_por_email(self, email: str) -> Usuario | None:
        """Busca um usuário pelo e-mail normalizado."""

    @abstractmethod
    def buscar_por_id(self, usuario_id: UUID) -> Usuario | None:
        """Busca um usuário pelo identificador."""

    @abstractmethod
    def listar(self, offset: int, limite: int) -> list[Usuario]:
        """Lista usuários de forma paginada."""

    @abstractmethod
    def contar(self) -> int:
        """Retorna a quantidade total de usuários."""

    @abstractmethod
    def salvar(self, usuario: Usuario) -> Usuario:
        """Persiste um novo usuário."""

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> Usuario | None:
        """Atualiza um usuário existente."""
