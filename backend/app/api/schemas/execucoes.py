from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.enums.status_execucao import StatusExecucao


class IniciarExecucaoRequest(BaseModel):
    """Corpo vazio que rejeita campos controlados pelo backend."""

    model_config = ConfigDict(extra="forbid")


class ExecucaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    automacao_id: UUID
    equipe_id: UUID
    solicitada_por_usuario_id: UUID
    status: StatusExecucao
    mensagem_erro: str | None
    criada_em: datetime
    iniciada_em: datetime | None
    finalizada_em: datetime | None
    atualizada_em: datetime


class ListaExecucoesResponse(BaseModel):
    execucoes: list[ExecucaoResponse]
    pagina: int
    itens_por_pagina: int
    total: int
    total_paginas: int
