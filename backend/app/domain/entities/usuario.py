from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.perfil_acesso import PerfilAcesso


@dataclass(slots=True)
class Usuario:
    """Usuário da plataforma, independente do banco e do framework web."""

    id: UUID
    nome: str
    email: str
    senha_hash: str
    perfil_acesso: PerfilAcesso
    equipe_id: UUID | None
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
