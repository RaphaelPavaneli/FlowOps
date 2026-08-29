"""Criar schema operacao e tabela de automações.

Revision ID: 20260825_01
Revises: 20260824_01
Create Date: 2026-08-25
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260825_01"
down_revision: str | None = "20260824_01"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute(
        "IF SCHEMA_ID(N'operacao') IS NULL "
        "EXEC(N'CREATE SCHEMA operacao')"
    )
    op.create_table(
        "automacoes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=False),
        sa.Column("criada_por_usuario_id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.Unicode(length=120), nullable=False),
        sa.Column("nome_normalizado", sa.Unicode(length=120), nullable=False),
        sa.Column("descricao", sa.Unicode(length=500), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("criada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("atualizada_em", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('rascunho', 'ativa', 'pausada')",
            name="ck_operacao_automacoes_status",
        ),
        sa.ForeignKeyConstraint(
            ["equipe_id"],
            ["auth.equipes.id"],
            name="fk_operacao_automacoes_equipe_id",
        ),
        sa.ForeignKeyConstraint(
            ["criada_por_usuario_id"],
            ["auth.usuarios.id"],
            name="fk_operacao_automacoes_criador_id",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_operacao_automacoes"),
        schema="operacao",
    )
    op.create_index(
        "uq_operacao_automacoes_equipe_nome",
        "automacoes",
        ["equipe_id", "nome_normalizado"],
        unique=True,
        schema="operacao",
    )
    op.create_index(
        "ix_operacao_automacoes_equipe_criada_em",
        "automacoes",
        ["equipe_id", "criada_em", "id"],
        schema="operacao",
    )
    op.create_index(
        "ix_operacao_automacoes_criador",
        "automacoes",
        ["criada_por_usuario_id"],
        schema="operacao",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_operacao_automacoes_criador",
        table_name="automacoes",
        schema="operacao",
    )
    op.drop_index(
        "ix_operacao_automacoes_equipe_criada_em",
        table_name="automacoes",
        schema="operacao",
    )
    op.drop_index(
        "uq_operacao_automacoes_equipe_nome",
        table_name="automacoes",
        schema="operacao",
    )
    op.drop_table("automacoes", schema="operacao")
    op.execute(
        "IF EXISTS ("
        "SELECT 1 FROM sys.schemas WHERE name = N'operacao'"
        ") EXEC(N'DROP SCHEMA operacao')"
    )
