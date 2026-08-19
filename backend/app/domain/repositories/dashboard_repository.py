from abc import ABC, abstractmethod

from app.domain.value_objects.resumo_dashboard import ResumoDashboard


class DashboardRepository(ABC):
    """Contrato de leitura dos indicadores do dashboard."""

    @abstractmethod
    def obter_resumo(self) -> ResumoDashboard:
        """Obtém o resumo administrativo atual."""
