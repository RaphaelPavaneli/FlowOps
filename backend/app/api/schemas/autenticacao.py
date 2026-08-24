from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.enums.perfil_acesso import PerfilAcesso


NomeUsuario = Annotated[str, Field(min_length=2, max_length=120)]
SenhaUsuario = Annotated[str, Field(min_length=12, max_length=128)]


class CadastroRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: NomeUsuario
    email: EmailStr
    senha: SenhaUsuario

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, nome: str) -> str:
        nome_limpo = nome.strip()
        if len(nome_limpo) < 2:
            raise ValueError("O nome deve possuir pelo menos 2 caracteres.")
        return nome_limpo


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    senha: Annotated[str, Field(min_length=1, max_length=128)]


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    email: EmailStr
    perfil_acesso: PerfilAcesso
    equipe_id: UUID | None
    ativo: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int
