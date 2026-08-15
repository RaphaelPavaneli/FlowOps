"""Exceções de negócio."""

from app.domain.exceptions.autenticacao import (
    CredenciaisInvalidasError,
    EmailJaCadastradoError,
    OperacaoUsuarioNaoPermitidaError,
    TokenInvalidoError,
    UsuarioInativoError,
    UsuarioNaoEncontradoError,
)

__all__ = [
    "CredenciaisInvalidasError",
    "EmailJaCadastradoError",
    "OperacaoUsuarioNaoPermitidaError",
    "TokenInvalidoError",
    "UsuarioInativoError",
    "UsuarioNaoEncontradoError",
]
