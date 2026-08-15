from enum import StrEnum


class PerfilAcesso(StrEnum):
    """Papéis iniciais disponíveis para autorização."""

    ADMINISTRADOR = "administrador"
    USUARIO = "usuario"
