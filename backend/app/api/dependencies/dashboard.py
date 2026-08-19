from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.obter_resumo_dashboard_administrativo import (
    ObterResumoDashboardAdministrativo,
)
from app.domain.repositories.dashboard_repository import DashboardRepository
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.repositories.sql_dashboard_repository import (
    SqlDashboardRepository,
)


def get_dashboard_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> DashboardRepository:
    return SqlDashboardRepository(session)


def get_obter_resumo_dashboard_administrativo(
    repository: Annotated[
        DashboardRepository,
        Depends(get_dashboard_repository),
    ],
) -> ObterResumoDashboardAdministrativo:
    return ObterResumoDashboardAdministrativo(repository)
