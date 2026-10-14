from sqlalchemy.dialects import mssql
from sqlalchemy.schema import CreateIndex

from app.infrastructure.database.models.execucao_model import ExecucaoModel


def test_indice_de_execucao_ativa_usa_literais_varchar_no_sql_server() -> None:
    indice = next(
        indice
        for indice in ExecucaoModel.__table__.indexes
        if indice.name == "uq_operacao_execucoes_automacao_ativa"
    )

    ddl = str(CreateIndex(indice).compile(dialect=mssql.dialect()))

    assert "WHERE status IN ('pendente', 'processando')" in ddl
    assert "N'pendente'" not in ddl
    assert "N'processando'" not in ddl
