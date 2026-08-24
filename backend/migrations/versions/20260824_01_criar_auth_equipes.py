"""Criar equipes e associar usuários de forma opcional.

Revision ID: 20260824_01
Revises: 20260813_01
Create Date: 2026-08-24
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260824_01"
down_revision: str | None = "20260813_01"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "equipes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.Unicode(length=120), nullable=False),
        sa.Column("ativa", sa.Boolean(), nullable=False),
        sa.Column("criada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("atualizada_em", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_auth_equipes"),
        schema="auth",
    )
    op.create_index(
        "ix_auth_equipes_nome",
        "equipes",
        ["nome"],
        schema="auth",
    )
    op.add_column(
        "usuarios",
        sa.Column("equipe_id", sa.Uuid(), nullable=True),
        schema="auth",
    )
    op.create_foreign_key(
        "fk_auth_usuarios_equipe_id",
        "usuarios",
        "equipes",
        ["equipe_id"],
        ["id"],
        source_schema="auth",
        referent_schema="auth",
    )
    op.create_index(
        "ix_auth_usuarios_equipe_id",
        "usuarios",
        ["equipe_id"],
        schema="auth",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_auth_usuarios_equipe_id",
        table_name="usuarios",
        schema="auth",
    )
    op.drop_constraint(
        "fk_auth_usuarios_equipe_id",
        "usuarios",
        schema="auth",
        type_="foreignkey",
    )
    op.drop_column("usuarios", "equipe_id", schema="auth")
    op.drop_index(
        "ix_auth_equipes_nome",
        table_name="equipes",
        schema="auth",
    )
    op.drop_table("equipes", schema="auth")
