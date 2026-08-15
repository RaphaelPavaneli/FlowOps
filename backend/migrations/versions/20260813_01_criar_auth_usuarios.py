"""Criar schema auth e tabela de usuários.

Revision ID: 20260813_01
Revises:
Create Date: 2026-08-13
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260813_01"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute(
        "IF SCHEMA_ID(N'auth') IS NULL EXEC(N'CREATE SCHEMA auth')"
    )
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.Unicode(length=120), nullable=False),
        sa.Column("email", sa.Unicode(length=254), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("perfil_acesso", sa.String(length=30), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_auth_usuarios"),
        schema="auth",
    )
    op.create_index(
        "uq_auth_usuarios_email",
        "usuarios",
        ["email"],
        unique=True,
        schema="auth",
    )


def downgrade() -> None:
    op.drop_index(
        "uq_auth_usuarios_email",
        table_name="usuarios",
        schema="auth",
    )
    op.drop_table("usuarios", schema="auth")
    op.execute(
        "IF EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'auth') "
        "EXEC(N'DROP SCHEMA auth')"
    )
