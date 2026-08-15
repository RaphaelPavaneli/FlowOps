from pydantic import BaseModel, ConfigDict

from app.api.schemas.autenticacao import UsuarioResponse
from app.domain.enums.perfil_acesso import PerfilAcesso


class AlterarPerfilRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    perfil_acesso: PerfilAcesso


class AlterarStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ativo: bool


class ListaUsuariosResponse(BaseModel):
    usuarios: list[UsuarioResponse]
    pagina: int
    itens_por_pagina: int
    total: int
    total_paginas: int
