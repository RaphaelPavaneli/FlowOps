from pydantic import BaseModel

from app.core.settings import AppSettings, DatabaseSettings, JwtSettings


class Settings(BaseModel):
    """Centraliza as configurações por responsabilidade."""

    app: AppSettings
    db: DatabaseSettings
    jwt: JwtSettings


settings = Settings(
    app=AppSettings(),
    db=DatabaseSettings(),
    jwt=JwtSettings(),
)
