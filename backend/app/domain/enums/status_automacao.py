from enum import StrEnum


class StatusAutomacao(StrEnum):
    """Estados disponíveis para uma automação."""

    RASCUNHO = "rascunho"
    ATIVA = "ativa"
    PAUSADA = "pausada"
