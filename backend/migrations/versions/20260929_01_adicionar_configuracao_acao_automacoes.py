"""Adicionar configuração de ação às automações.

Revision ID: 20260929_01
Revises: 20260914_01
Create Date: 2026-09-29
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260929_01"
down_revision: str | None = "20260914_01"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.add_column(
        "automacoes",
        sa.Column(
            "tipo_acao",
            sa.String(length=50),
            nullable=False,
            server_default="teste_controlado",
        ),
        schema="operacao",
    )
    op.add_column(
        "automacoes",
        sa.Column(
            "configuracao_acao",
            sa.Unicode(length=500),
            nullable=False,
            server_default='{"resultado":"sucesso"}',
        ),
        schema="operacao",
    )
    op.create_check_constraint(
        "ck_operacao_automacoes_tipo_acao",
        "automacoes",
        "tipo_acao IN ('teste_controlado')",
        schema="operacao",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_operacao_automacoes_tipo_acao",
        "automacoes",
        schema="operacao",
        type_="check",
    )
    op.drop_column(
        "automacoes",
        "configuracao_acao",
        schema="operacao",
    )
    op.drop_column(
        "automacoes",
        "tipo_acao",
        schema="operacao",
    )
