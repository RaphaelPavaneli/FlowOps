from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Contrato para criação e verificação segura de senhas."""

    @abstractmethod
    def gerar_hash(self, senha: str) -> str:
        """Gera um hash não reversível para a senha."""

    @abstractmethod
    def verificar(self, senha: str, senha_hash: str | None) -> bool:
        """Verifica a senha e simula o custo quando o usuário não existe."""
