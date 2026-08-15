class EmailJaCadastradoError(Exception):
    """Indica uma tentativa de cadastrar um e-mail já utilizado."""


class CredenciaisInvalidasError(Exception):
    """Representa uma falha de autenticação sem revelar qual dado falhou."""


class TokenInvalidoError(Exception):
    """Indica que um token não pôde ser validado."""


class UsuarioNaoEncontradoError(Exception):
    """Indica que o usuário do token não existe mais."""


class UsuarioInativoError(Exception):
    """Indica que o usuário não pode mais acessar a aplicação."""


class OperacaoUsuarioNaoPermitidaError(Exception):
    """Impede que um administrador remova o próprio acesso."""
