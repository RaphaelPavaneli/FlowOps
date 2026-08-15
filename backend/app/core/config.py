from typing import Literal

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FLOWOPS_",
        env_ignore_empty=True,
        extra="ignore",
    )

    app_name: str = "FlowOps API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    db_server: str = "localhost"
    db_port: int | None = None
    db_name: str = "DB_FLOWOPS"
    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_auth_mode: Literal["windows", "sql"] = "windows"
    db_user: str | None = None
    db_password: SecretStr | None = None
    db_encrypt: bool = True
    db_trust_server_certificate: bool = True

    jwt_secret_key: SecretStr
    jwt_algorithm: Literal["HS256"] = "HS256"
    jwt_issuer: str = "flowops-api"
    jwt_audience: str = "flowops-web"
    access_token_expire_minutes: int = 15

    @model_validator(mode="after")
    def validar_credenciais_banco(self) -> "Settings":
        if self.db_auth_mode == "sql":
            senha = (
                self.db_password.get_secret_value()
                if self.db_password is not None
                else ""
            )
            if not self.db_user or not senha:
                raise ValueError(
                    "FLOWOPS_DB_USER e FLOWOPS_DB_PASSWORD são obrigatórios "
                    "quando FLOWOPS_DB_AUTH_MODE=sql."
                )
        return self

    @field_validator("jwt_secret_key")
    @classmethod
    def validar_jwt_secret_key(cls, secret_key: SecretStr) -> SecretStr:
        valor = secret_key.get_secret_value()
        if len(valor) < 32 or valor.startswith("substitua-"):
            raise ValueError(
                "FLOWOPS_JWT_SECRET_KEY deve ser uma chave aleatória com "
                "pelo menos 32 caracteres."
            )
        return secret_key


settings = Settings()
