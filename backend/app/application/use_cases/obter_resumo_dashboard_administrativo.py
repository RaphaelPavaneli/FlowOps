from app.domain.repositories.dashboard_repository import DashboardRepository
from app.domain.value_objects.resumo_dashboard import ResumoDashboard


class ObterResumoDashboardAdministrativo:
    """Obtém os indicadores visíveis para administradores."""

    def __init__(self, dashboard_repository: DashboardRepository) -> None:
        self._dashboard_repository = dashboard_repository

    def executar(self) -> ResumoDashboard:
        return self._dashboard_repository.obter_resumo()
