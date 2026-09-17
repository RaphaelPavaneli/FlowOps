from enum import StrEnum


class StatusExecucao(StrEnum):
    """Estados disponíveis para uma execução de automação."""

    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    CONCLUIDA = "concluida"
    FALHOU = "falhou"
