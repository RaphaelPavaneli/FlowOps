from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Index, String, Unicode, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class UsuarioModel(Base):
    """Representação SQLAlchemy da tabela de usuários."""

    __tablename__ = "usuarios"
    __table_args__ = (
        Index("uq_auth_usuarios_email", "email", unique=True),
        {"schema": "auth"},
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Unicode(120), nullable=False)
    email: Mapped[str] = mapped_column(
        Unicode(254),
        nullable=False,
    )
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil_acesso: Mapped[str] = mapped_column(String(30), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
