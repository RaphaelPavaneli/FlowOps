import pytest
from pydantic import ValidationError

from app.core.settings import AppSettings, DatabaseSettings, JwtSettings
from app.infrastructure.database.connection import build_database_url


JWT_SECRET_TESTE = "chave-de-testes-com-pelo-menos-32-caracteres"


def test_conexao_sql_usa_configuracoes_estaveis() -> None:
    configuracao = DatabaseSettings(
        _env_file=None,
        server="localhost",
        port=1433,
        name="DB_FLOWOPS",
        user="flowops_app",
        password="senha-segura",
    )

    url = build_database_url(configuracao)

    assert url.drivername == "mssql+pyodbc"
    assert url.host == "localhost"
    assert url.port == 1433
    assert url.database == "DB_FLOWOPS"
    assert url.username == "flowops_app"
    assert url.password == "senha-segura"
    assert url.query["driver"] == "ODBC Driver 18 for SQL Server"
    assert url.query["Encrypt"] == "yes"
    assert url.query["TrustServerCertificate"] == "no"
    assert "Trusted_Connection" not in url.query


def test_conexao_sql_preserva_credenciais_com_caracteres_especiais() -> None:
    configuracao = DatabaseSettings(
        _env_file=None,
        server="localhost",
        name="DB_FLOWOPS",
        user="flowops_app",
        password="S@nh:a/segura#123",
    )

    url = build_database_url(configuracao)

    assert url.username == "flowops_app"
    assert url.password == "S@nh:a/segura#123"
    assert "S@nh:a/segura#123" not in str(url)


def test_conexao_sql_exige_usuario_e_senha(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)

    with pytest.raises(ValidationError) as erro:
        DatabaseSettings(
            _env_file=None,
            server="localhost",
            name="DB_FLOWOPS",
        )

    campos_invalidos = {
        item["loc"][0]
        for item in erro.value.errors()
    }
    assert campos_invalidos == {"user", "password"}


def test_certificado_pode_ser_confiado_no_desenvolvimento() -> None:
    configuracao = DatabaseSettings(
        _env_file=None,
        server="localhost",
        name="DB_FLOWOPS",
        user="flowops_app",
        password="senha-segura",
        trust_server_certificate=True,
    )

    url = build_database_url(configuracao)

    assert url.query["TrustServerCertificate"] == "yes"


def test_configuracoes_estaveis_da_aplicacao_e_jwt() -> None:
    app = AppSettings()
    jwt = JwtSettings(
        _env_file=None,
        secret_key=JWT_SECRET_TESTE,
    )

    assert app.name == "FlowOps API"
    assert app.version == "0.1.0"
    assert app.api_v1_prefix == "/api/v1"
    assert jwt.algorithm == "HS256"
    assert jwt.issuer == "flowops-api"
    assert jwt.audience == "flowops-web"
    assert jwt.access_token_expire_minutes == 15
