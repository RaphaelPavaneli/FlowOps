import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.infrastructure.database.connection import build_database_url


JWT_SECRET_TESTE = "chave-de-testes-com-pelo-menos-32-caracteres"


def test_conexao_windows_usa_driver_e_autenticacao_integrada() -> None:
    configuracao = Settings(
        _env_file=None,
        jwt_secret_key=JWT_SECRET_TESTE,
        db_server="localhost",
        db_name="DB_FLOWOPS",
        db_auth_mode="windows",
    )

    url = build_database_url(configuracao)

    assert url.drivername == "mssql+pyodbc"
    assert url.host == "localhost"
    assert url.database == "DB_FLOWOPS"
    assert url.username is None
    assert url.password is None
    assert url.query["driver"] == "ODBC Driver 18 for SQL Server"
    assert url.query["Trusted_Connection"] == "yes"


def test_conexao_sql_preserva_credenciais_com_caracteres_especiais() -> None:
    configuracao = Settings(
        _env_file=None,
        jwt_secret_key=JWT_SECRET_TESTE,
        db_auth_mode="sql",
        db_user="flowops_app",
        db_password="S@nh:a/segura#123",
    )

    url = build_database_url(configuracao)

    assert url.username == "flowops_app"
    assert url.password == "S@nh:a/segura#123"
    assert "Trusted_Connection" not in url.query
    assert "S@nh:a/segura#123" not in str(url)


def test_conexao_sql_exige_usuario_e_senha() -> None:
    with pytest.raises(ValidationError, match="FLOWOPS_DB_USER"):
        Settings(
            _env_file=None,
            jwt_secret_key=JWT_SECRET_TESTE,
            db_auth_mode="sql",
        )
