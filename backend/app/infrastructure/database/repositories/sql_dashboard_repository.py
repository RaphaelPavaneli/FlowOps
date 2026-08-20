from sqlalchemy import case, func, select, true, false
from sqlalchemy.orm import Session

from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.repositories.dashboard_repository import DashboardRepository
from app.domain.value_objects.resumo_dashboard import (
    ResumoDashboard,
    ResumoUsuarios,
)
from app.infrastructure.database.models.usuario_model import UsuarioModel


class SqlDashboardRepository(DashboardRepository):
    """Consulta os indicadores do dashboard usando SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def obter_resumo(self) -> ResumoDashboard:
        resultado = self._session.execute(
            select(
                func.count(UsuarioModel.id).label("total"),
                self._somar_quando(UsuarioModel.ativo == true()).label(
                    "ativos"
                ),
                self._somar_quando(UsuarioModel.ativo == false()).label(
                    "inativos"
                ),
                self._somar_quando(
                    UsuarioModel.perfil_acesso
                    == PerfilAcesso.ADMINISTRADOR.value
                ).label("administradores"),
                self._somar_quando(
                    UsuarioModel.perfil_acesso == PerfilAcesso.USUARIO.value
                ).label("comuns"),
            )
        ).one()

        return ResumoDashboard(
            usuarios=ResumoUsuarios(
                total=int(resultado.total or 0),
                ativos=int(resultado.ativos or 0),
                inativos=int(resultado.inativos or 0),
                administradores=int(resultado.administradores or 0),
                comuns=int(resultado.comuns or 0),
            )
        )

    @staticmethod
    def _somar_quando(condicao):
        return func.coalesce(func.sum(case((condicao, 1), else_=0)), 0)
