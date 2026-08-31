class UsuarioSemEquipeError(Exception):
    """Indica que o usuário ainda não possui contexto operacional."""


class EquipeUsuarioIndisponivelError(Exception):
    """Indica que a equipe do usuário não existe ou está inativa."""


class AutomacaoNomeDuplicadoError(Exception):
    """Impede nomes repetidos dentro da mesma equipe."""
