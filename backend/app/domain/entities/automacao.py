from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.exceptions.automacoes import (
    TransicaoStatusAutomacaoInvalidaError,
)


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

    def ativar(self, momento: datetime) -> None:
        """Ativa uma automação em rascunho ou pausada."""
        if self.status not in {
            StatusAutomacao.RASCUNHO,
            StatusAutomacao.PAUSADA,
        }:
            raise TransicaoStatusAutomacaoInvalidaError(
                self.status,
                StatusAutomacao.ATIVA,
            )

        self.status = StatusAutomacao.ATIVA
        self.atualizada_em = momento

    def pausar(self, momento: datetime) -> None:
        """Pausa uma automação que está ativa."""
        if self.status is not StatusAutomacao.ATIVA:
            raise TransicaoStatusAutomacaoInvalidaError(
                self.status,
                StatusAutomacao.PAUSADA,
            )

        self.status = StatusAutomacao.PAUSADA
        self.atualizada_em = momento
