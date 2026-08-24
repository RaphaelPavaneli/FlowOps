from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.entities.equipe import Equipe
from app.domain.repositories.equipe_repository import EquipeRepository
from app.infrastructure.database.models.equipe_model import EquipeModel


class SqlEquipeRepository(EquipeRepository):
    """Persistência de equipes utilizando SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def buscar_por_id(self, equipe_id: UUID) -> Equipe | None:
        modelo = self._session.get(EquipeModel, equipe_id)
        return self._para_entidade(modelo) if modelo else None

    def listar(self, offset: int, limite: int) -> list[Equipe]:
        modelos = self._session.scalars(
            select(EquipeModel)
            .order_by(EquipeModel.nome, EquipeModel.id)
            .offset(offset)
            .limit(limite)
        ).all()
        return [self._para_entidade(modelo) for modelo in modelos]

    def contar(self) -> int:
        return self._session.scalar(
            select(func.count()).select_from(EquipeModel)
        ) or 0

    def salvar(self, equipe: Equipe) -> Equipe:
        modelo = EquipeModel(
            id=equipe.id,
            nome=equipe.nome,
            ativa=equipe.ativa,
            criada_em=equipe.criada_em,
            atualizada_em=equipe.atualizada_em,
        )
        self._session.add(modelo)
        self._session.commit()
        self._session.refresh(modelo)
        return self._para_entidade(modelo)

    @staticmethod
    def _para_entidade(modelo: EquipeModel) -> Equipe:
        return Equipe(
            id=modelo.id,
            nome=modelo.nome,
            ativa=modelo.ativa,
            criada_em=modelo.criada_em,
            atualizada_em=modelo.atualizada_em,
        )
