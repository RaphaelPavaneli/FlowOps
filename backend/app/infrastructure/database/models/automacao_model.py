from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Unicode,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class AutomacaoModel(Base):
    """Representação SQLAlchemy da tabela de automações."""

    __tablename__ = "automacoes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('rascunho', 'ativa', 'pausada')",
            name="ck_operacao_automacoes_status",
        ),
        Index(
            "uq_operacao_automacoes_equipe_nome",
            "equipe_id",
            "nome_normalizado",
            unique=True,
        ),
        Index(
            "ix_operacao_automacoes_equipe_criada_em",
            "equipe_id",
            "criada_em",
            "id",
        ),
        Index(
            "ix_operacao_automacoes_criador",
            "criada_por_usuario_id",
        ),
        {"schema": "operacao"},
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    equipe_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "auth.equipes.id",
            name="fk_operacao_automacoes_equipe_id",
        ),
        nullable=False,
    )
    criada_por_usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "auth.usuarios.id",
            name="fk_operacao_automacoes_criador_id",
        ),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(Unicode(120), nullable=False)
    nome_normalizado: Mapped[str] = mapped_column(
        Unicode(120),
        nullable=False,
    )
    descricao: Mapped[str | None] = mapped_column(
        Unicode(500),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    atualizada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
