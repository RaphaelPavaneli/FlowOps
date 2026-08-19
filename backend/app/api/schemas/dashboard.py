from pydantic import BaseModel, ConfigDict


class ResumoUsuariosResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    ativos: int
    inativos: int
    administradores: int
    comuns: int


class ResumoDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuarios: ResumoUsuariosResponse
