from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.resultado_teste_controlado import (
    ResultadoTesteControlado,
)
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao


NomeAutomacao = Annotated[str, Field(min_length=2, max_length=120)]
DescricaoAutomacao = Annotated[str | None, Field(max_length=500)]


class ConfiguracaoTesteControladoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    resultado: ResultadoTesteControlado = ResultadoTesteControlado.SUCESSO


class CriarAutomacaoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: NomeAutomacao
    descricao: DescricaoAutomacao = None
    tipo_acao: TipoAcaoAutomacao = TipoAcaoAutomacao.TESTE_CONTROLADO
    configuracao_acao: ConfiguracaoTesteControladoSchema = Field(
        default_factory=ConfiguracaoTesteControladoSchema
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, nome: str) -> str:
        nome_limpo = " ".join(nome.split())
        if len(nome_limpo) < 2:
            raise ValueError("O nome deve possuir pelo menos 2 caracteres.")
        return nome_limpo

    @field_validator("descricao")
    @classmethod
    def limpar_descricao(cls, descricao: str | None) -> str | None:
        if descricao is None:
            return None
        return descricao.strip() or None


class AutomacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    equipe_id: UUID
    criada_por_usuario_id: UUID
    nome: str
    descricao: str | None
    tipo_acao: TipoAcaoAutomacao
    configuracao_acao: ConfiguracaoTesteControladoSchema
    status: StatusAutomacao
    criada_em: datetime
    atualizada_em: datetime


class ListaAutomacoesResponse(BaseModel):
    automacoes: list[AutomacaoResponse]
    pagina: int
    itens_por_pagina: int
    total: int
    total_paginas: int
