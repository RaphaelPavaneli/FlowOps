from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configurações da conexão SQL Server carregadas do ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DB_",
        env_ignore_empty=True,
        extra="ignore",
    )

    server: str
    port: int | None = None
    name: str
    user: str
    password: SecretStr

    driver: str = "ODBC Driver 18 for SQL Server"
    encrypt: bool = True
    trust_server_certificate: bool = False
