from app.domain.enums.status_automacao import StatusAutomacao


class UsuarioSemEquipeError(Exception):
    """Indica que o usuário ainda não possui contexto operacional."""


class EquipeUsuarioIndisponivelError(Exception):
    """Indica que a equipe do usuário não existe ou está inativa."""


class AutomacaoNomeDuplicadoError(Exception):
    """Impede nomes repetidos dentro da mesma equipe."""


class AutomacaoNaoEncontradaError(Exception):
    """Evita revelar automações ausentes ou pertencentes a outra equipe."""


class AutomacaoIndisponivelParaExecucaoError(Exception):
    """Impede iniciar execuções de automações que não estão ativas."""


class TransicaoStatusAutomacaoInvalidaError(Exception):
    """Impede uma transição não permitida no ciclo da automação."""

    def __init__(
        self,
        status_atual: StatusAutomacao,
        status_destino: StatusAutomacao,
    ) -> None:
        self.status_atual = status_atual
        self.status_destino = status_destino
        super().__init__(
            "Não é possível alterar a automação de "
            f"'{status_atual.value}' para '{status_destino.value}'."
        )
