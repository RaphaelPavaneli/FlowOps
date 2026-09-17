from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.database.models.execucao_model import ExecucaoModel


class SqlExecucaoRepository(ExecucaoRepository):
    """Persiste execuções mantendo o isolamento obrigatório por equipe."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def salvar(self, execucao: Execucao) -> Execucao:
        modelo = ExecucaoModel(
            id=execucao.id,
            automacao_id=execucao.automacao_id,
            equipe_id=execucao.equipe_id,
            solicitada_por_usuario_id=(
                execucao.solicitada_por_usuario_id
            ),
            status=execucao.status.value,
            mensagem_erro=execucao.mensagem_erro,
            criada_em=execucao.criada_em,
            iniciada_em=execucao.iniciada_em,
            finalizada_em=execucao.finalizada_em,
            atualizada_em=execucao.atualizada_em,
        )
        self._session.add(modelo)
        self._session.commit()
        self._session.refresh(modelo)
        return self._para_entidade(modelo)

    def atualizar(self, execucao: Execucao) -> Execucao | None:
        modelo = self._session.scalar(
            select(ExecucaoModel).where(
                ExecucaoModel.id == execucao.id,
                ExecucaoModel.equipe_id == execucao.equipe_id,
            )
        )
        if modelo is None:
            return None

        modelo.status = execucao.status.value
        modelo.mensagem_erro = execucao.mensagem_erro
        modelo.iniciada_em = execucao.iniciada_em
        modelo.finalizada_em = execucao.finalizada_em
        modelo.atualizada_em = execucao.atualizada_em
        self._session.commit()
        self._session.refresh(modelo)
        return self._para_entidade(modelo)

    def buscar_por_id_e_equipe(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
    ) -> Execucao | None:
        modelo = self._session.scalar(
            select(ExecucaoModel).where(
                ExecucaoModel.id == execucao_id,
                ExecucaoModel.equipe_id == equipe_id,
            )
        )
        return self._para_entidade(modelo) if modelo else None

    def listar_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
        offset: int,
        limite: int,
    ) -> list[Execucao]:
        modelos = self._session.scalars(
            select(ExecucaoModel)
            .where(
                ExecucaoModel.automacao_id == automacao_id,
                ExecucaoModel.equipe_id == equipe_id,
            )
            .order_by(
                ExecucaoModel.criada_em.desc(),
                ExecucaoModel.id,
            )
            .offset(offset)
            .limit(limite)
        ).all()
        return [self._para_entidade(modelo) for modelo in modelos]

    def contar_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
    ) -> int:
        return self._session.scalar(
            select(func.count())
            .select_from(ExecucaoModel)
            .where(
                ExecucaoModel.automacao_id == automacao_id,
                ExecucaoModel.equipe_id == equipe_id,
            )
        ) or 0

    @staticmethod
    def _para_entidade(modelo: ExecucaoModel) -> Execucao:
        return Execucao(
            id=modelo.id,
            automacao_id=modelo.automacao_id,
            equipe_id=modelo.equipe_id,
            solicitada_por_usuario_id=(
                modelo.solicitada_por_usuario_id
            ),
            status=StatusExecucao(modelo.status),
            mensagem_erro=modelo.mensagem_erro,
            criada_em=modelo.criada_em,
            iniciada_em=modelo.iniciada_em,
            finalizada_em=modelo.finalizada_em,
            atualizada_em=modelo.atualizada_em,
        )
