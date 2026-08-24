from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Equipe:
    """Equipe que delimita o compartilhamento dos dados operacionais."""

    id: UUID
    nome: str
    ativa: bool
    criada_em: datetime
    atualizada_em: datetime
