from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


NomeEquipe = Annotated[str, Field(min_length=2, max_length=120)]


class CriarEquipeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: NomeEquipe

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, nome: str) -> str:
        nome_limpo = nome.strip()
        if len(nome_limpo) < 2:
            raise ValueError("O nome deve possuir pelo menos 2 caracteres.")
        return nome_limpo


class EquipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    ativa: bool
    criada_em: datetime
    atualizada_em: datetime


class ListaEquipesResponse(BaseModel):
    equipes: list[EquipeResponse]
    pagina: int
    itens_por_pagina: int
    total: int
    total_paginas: int
