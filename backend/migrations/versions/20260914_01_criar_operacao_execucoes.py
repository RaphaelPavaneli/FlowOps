"""Criar tabela de execuções de automações.

Revision ID: 20260914_01
Revises: 20260825_01
Create Date: 2026-09-14
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260914_01"
down_revision: str | None = "20260825_01"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "execucoes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("automacao_id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=False),
        sa.Column("solicitada_por_usuario_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("mensagem_erro", sa.Unicode(length=2000), nullable=True),
        sa.Column("criada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("iniciada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finalizada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("atualizada_em", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('pendente', 'processando', 'concluida', 'falhou')",
            name="ck_operacao_execucoes_status",
        ),
        sa.ForeignKeyConstraint(
            ["automacao_id"],
            ["operacao.automacoes.id"],
            name="fk_operacao_execucoes_automacao_id",
        ),
        sa.ForeignKeyConstraint(
            ["equipe_id"],
            ["auth.equipes.id"],
            name="fk_operacao_execucoes_equipe_id",
        ),
        sa.ForeignKeyConstraint(
            ["solicitada_por_usuario_id"],
            ["auth.usuarios.id"],
            name="fk_operacao_execucoes_solicitante_id",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_operacao_execucoes"),
        schema="operacao",
    )
    op.create_index(
        "ix_operacao_execucoes_equipe_automacao_criada_em",
        "execucoes",
        ["equipe_id", "automacao_id", "criada_em", "id"],
        schema="operacao",
    )
    op.create_index(
        "ix_operacao_execucoes_equipe_status_criada_em",
        "execucoes",
        ["equipe_id", "status", "criada_em", "id"],
        schema="operacao",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_operacao_execucoes_equipe_status_criada_em",
        table_name="execucoes",
        schema="operacao",
    )
    op.drop_index(
        "ix_operacao_execucoes_equipe_automacao_criada_em",
        table_name="execucoes",
        schema="operacao",
    )
    op.drop_table("execucoes", schema="operacao")
