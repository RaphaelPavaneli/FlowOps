from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Unicode, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class ExecucaoModel(Base):
    """Representa a persistência de uma execução de automação."""

    __tablename__ = "execucoes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pendente', 'processando', 'concluida', 'falhou')",
            name="ck_operacao_execucoes_status",
        ),
        Index(
            "ix_operacao_execucoes_equipe_automacao_criada_em",
            "equipe_id",
            "automacao_id",
            "criada_em",
            "id",
        ),
        Index(
            "ix_operacao_execucoes_equipe_status_criada_em",
            "equipe_id",
            "status",
            "criada_em",
            "id",
        ),
        {"schema": "operacao"},
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    automacao_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "operacao.automacoes.id",
            name="fk_operacao_execucoes_automacao_id",
        ),
        nullable=False,
    )
    equipe_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "auth.equipes.id",
            name="fk_operacao_execucoes_equipe_id",
        ),
        nullable=False,
    )
    solicitada_por_usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "auth.usuarios.id",
            name="fk_operacao_execucoes_solicitante_id",
        ),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    mensagem_erro: Mapped[str | None] = mapped_column(
        Unicode(2000),
        nullable=True,
    )
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    iniciada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    finalizada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    atualizada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
