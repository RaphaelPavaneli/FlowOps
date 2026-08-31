from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Index, Unicode, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class EquipeModel(Base):
    """Representação SQLAlchemy da tabela de equipes."""

    __tablename__ = "equipes"
    __table_args__ = (
        Index("ix_auth_equipes_nome", "nome"),
        {"schema": "auth"},
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Unicode(120), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    atualizada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
