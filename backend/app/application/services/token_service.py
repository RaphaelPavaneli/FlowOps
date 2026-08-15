from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.perfil_acesso import PerfilAcesso


@dataclass(frozen=True, slots=True)
class DadosTokenAcesso:
    token: str
    expira_em_segundos: int


class TokenService(ABC):
    """Contrato para emissão e leitura de tokens de acesso."""

    @abstractmethod
    def criar_token_acesso(
        self,
        usuario_id: UUID,
        perfil_acesso: PerfilAcesso,
    ) -> DadosTokenAcesso:
        """Cria um token de acesso assinado."""

    @abstractmethod
    def obter_usuario_id(self, token: str) -> UUID:
        """Valida o token e retorna o identificador do usuário."""
