class EquipeNaoEncontradaError(Exception):
    """Indica que a equipe informada não existe."""


class EquipeInativaError(Exception):
    """Impede a associação de usuários a uma equipe inativa."""
