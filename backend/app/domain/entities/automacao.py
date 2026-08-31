from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.status_automacao import StatusAutomacao


@dataclass(slots=True)
class Automacao:
    """Automação compartilhada dentro de uma equipe."""

    id: UUID
    equipe_id: UUID
    criada_por_usuario_id: UUID
    nome: str
    nome_normalizado: str
    descricao: str | None
    status: StatusAutomacao
    criada_em: datetime
    atualizada_em: datetime
