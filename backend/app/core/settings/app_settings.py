from pydantic import BaseModel


class AppSettings(BaseModel):
    """Configurações estáveis da aplicação."""

    name: str = "FlowOps API"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
