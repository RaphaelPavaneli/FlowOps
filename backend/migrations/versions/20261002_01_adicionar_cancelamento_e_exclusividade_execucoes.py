"""Adicionar cancelamento e exclusividade às execuções.

Revision ID: 20261002_01
Revises: 20260929_01
Create Date: 2026-10-02
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20261002_01"
down_revision: str | None = "20260929_01"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            IF EXISTS (
                SELECT automacao_id
                FROM operacao.execucoes
                WHERE status IN (N'pendente', N'processando')
                GROUP BY automacao_id
                HAVING COUNT(*) > 1
            )
            BEGIN
                THROW 51030,
                    N'Existem automações com mais de uma execução ativa.',
                    1;
            END;
            """
        )
    )
    op.drop_constraint(
        "ck_operacao_execucoes_status",
        "execucoes",
        schema="operacao",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operacao_execucoes_status",
        "execucoes",
        "status IN ('pendente', 'processando', 'concluida', "
        "'falhou', 'cancelada')",
        schema="operacao",
    )
    op.create_index(
        "uq_operacao_execucoes_automacao_ativa",
        "execucoes",
        ["automacao_id"],
        unique=True,
        schema="operacao",
        mssql_where=sa.text("status IN ('pendente', 'processando')"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_operacao_execucoes_automacao_ativa",
        table_name="execucoes",
        schema="operacao",
    )
    op.execute(
        sa.text(
            """
            UPDATE operacao.execucoes
            SET status = N'falhou',
                mensagem_erro = COALESCE(
                    mensagem_erro,
                    N'A execução havia sido cancelada.'
                )
            WHERE status = N'cancelada';
            """
        )
    )
    op.drop_constraint(
        "ck_operacao_execucoes_status",
        "execucoes",
        schema="operacao",
        type_="check",
    )
    op.create_check_constraint(
        "ck_operacao_execucoes_status",
        "execucoes",
        "status IN ('pendente', 'processando', 'concluida', 'falhou')",
        schema="operacao",
    )
