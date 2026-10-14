from app.domain.enums.status_execucao import StatusExecucao


class TransicaoStatusExecucaoInvalidaError(Exception):
    """Impede uma transição não permitida no ciclo da execução."""

    def __init__(
        self,
        status_atual: StatusExecucao,
        status_destino: StatusExecucao,
    ) -> None:
        self.status_atual = status_atual
        self.status_destino = status_destino
        super().__init__(
            "Não é possível alterar a execução de "
            f"'{status_atual.value}' para '{status_destino.value}'."
        )


class MensagemFalhaExecucaoObrigatoriaError(Exception):
    """Exige uma mensagem útil ao registrar a falha da execução."""


class ExecucaoNaoEncontradaError(Exception):
    """Evita revelar execuções ausentes ou pertencentes a outra equipe."""


class ExecucaoEmAndamentoError(Exception):
    """Impede mais de uma execução ativa para a mesma automação."""


class ExecucaoIndisponivelParaCancelamentoError(Exception):
    """Impede o cancelamento de uma execução em estado terminal."""


class FalhaAoAgendarExecucaoError(Exception):
    """Informa que a execução persistida não pôde ser despachada."""
