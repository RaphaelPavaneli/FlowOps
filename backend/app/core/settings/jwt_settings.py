from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    """Configurações de emissão e validação dos tokens JWT."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JWT_",
        env_ignore_empty=True,
        extra="ignore",
    )

    secret_key: SecretStr
    algorithm: Literal["HS256"] = "HS256"
    issuer: str = "flowops-api"
    audience: str = "flowops-web"
    access_token_expire_minutes: int = 15

    @field_validator("secret_key")
    @classmethod
    def validar_secret_key(cls, secret_key: SecretStr) -> SecretStr:
        valor = secret_key.get_secret_value()
        if len(valor) < 32 or valor.startswith("substitua-"):
            raise ValueError(
                "JWT_SECRET_KEY deve ser uma chave aleatória com "
                "pelo menos 32 caracteres."
            )
        return secret_key
