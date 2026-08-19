from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.autorizacao import exigir_perfil
from app.api.dependencies.dashboard import (
    get_obter_resumo_dashboard_administrativo,
)
from app.api.schemas.dashboard import ResumoDashboardResponse
from app.application.use_cases.obter_resumo_dashboard_administrativo import (
    ObterResumoDashboardAdministrativo,
)
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
administrador_required = exigir_perfil(PerfilAcesso.ADMINISTRADOR)


@router.get(
    "/resumo-administrativo",
    response_model=ResumoDashboardResponse,
    summary="Obter resumo administrativo do dashboard",
)
def obter_resumo_dashboard_administrativo(
    administrador: Annotated[Usuario, Depends(administrador_required)],
    caso_de_uso: Annotated[
        ObterResumoDashboardAdministrativo,
        Depends(get_obter_resumo_dashboard_administrativo),
    ],
) -> ResumoDashboardResponse:
    resumo = caso_de_uso.executar()
    return ResumoDashboardResponse.model_validate(resumo)
