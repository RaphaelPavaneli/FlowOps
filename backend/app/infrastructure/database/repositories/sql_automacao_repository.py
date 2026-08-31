from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.entities.automacao import Automacao
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.exceptions.automacoes import AutomacaoNomeDuplicadoError
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.infrastructure.database.models.automacao_model import AutomacaoModel


class SqlAutomacaoRepository(AutomacaoRepository):
    """Persistência de automações com isolamento obrigatório por equipe."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def buscar_por_nome_normalizado(
        self,
        equipe_id: UUID,
        nome_normalizado: str,
    ) -> Automacao | None:
        modelo = self._session.scalar(
            select(AutomacaoModel).where(
                AutomacaoModel.equipe_id == equipe_id,
                AutomacaoModel.nome_normalizado == nome_normalizado,
            )
        )
        return self._para_entidade(modelo) if modelo else None

    def listar_por_equipe(
        self,
        equipe_id: UUID,
        offset: int,
        limite: int,
    ) -> list[Automacao]:
        modelos = self._session.scalars(
            select(AutomacaoModel)
            .where(AutomacaoModel.equipe_id == equipe_id)
            .order_by(
                AutomacaoModel.criada_em.desc(),
                AutomacaoModel.id,
            )
            .offset(offset)
            .limit(limite)
        ).all()
        return [self._para_entidade(modelo) for modelo in modelos]

    def contar_por_equipe(self, equipe_id: UUID) -> int:
        return self._session.scalar(
            select(func.count())
            .select_from(AutomacaoModel)
            .where(AutomacaoModel.equipe_id == equipe_id)
        ) or 0

    def salvar(self, automacao: Automacao) -> Automacao:
        modelo = AutomacaoModel(
            id=automacao.id,
            equipe_id=automacao.equipe_id,
            criada_por_usuario_id=automacao.criada_por_usuario_id,
            nome=automacao.nome,
            nome_normalizado=automacao.nome_normalizado,
            descricao=automacao.descricao,
            status=automacao.status.value,
            criada_em=automacao.criada_em,
            atualizada_em=automacao.atualizada_em,
        )
        self._session.add(modelo)
        try:
            self._session.commit()
        except IntegrityError as erro:
            self._session.rollback()
            raise AutomacaoNomeDuplicadoError from erro

        self._session.refresh(modelo)
        return self._para_entidade(modelo)

    @staticmethod
    def _para_entidade(modelo: AutomacaoModel) -> Automacao:
        return Automacao(
            id=modelo.id,
            equipe_id=modelo.equipe_id,
            criada_por_usuario_id=modelo.criada_por_usuario_id,
            nome=modelo.nome,
            nome_normalizado=modelo.nome_normalizado,
            descricao=modelo.descricao,
            status=StatusAutomacao(modelo.status),
            criada_em=modelo.criada_em,
            atualizada_em=modelo.atualizada_em,
        )
