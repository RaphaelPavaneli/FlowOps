from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.services.password_hasher import PasswordHasher
from app.application.services.token_service import TokenService
from app.application.use_cases.autenticar_usuario import AutenticarUsuario
from app.application.use_cases.cadastrar_usuario import CadastrarUsuario
from app.application.use_cases.obter_usuario_atual import ObterUsuarioAtual
from app.core.config import settings
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.autenticacao import (
    TokenInvalidoError,
    UsuarioInativoError,
    UsuarioNaoEncontradoError,
)
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.repositories.sql_usuario_repository import (
    SqlUsuarioRepository,
)
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from app.infrastructure.security.jwt_token_service import JwtTokenService


bearer_scheme = HTTPBearer(auto_error=False)
password_hasher = Argon2PasswordHasher()


def get_usuario_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> UsuarioRepository:
    return SqlUsuarioRepository(session)


def get_password_hasher() -> PasswordHasher:
    return password_hasher


def get_token_service() -> TokenService:
    return JwtTokenService(
        secret_key=settings.jwt.secret_key.get_secret_value(),
        algorithm=settings.jwt.algorithm,
        issuer=settings.jwt.issuer,
        audience=settings.jwt.audience,
        expire_minutes=settings.jwt.access_token_expire_minutes,
    )


def get_cadastrar_usuario(
    repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> CadastrarUsuario:
    return CadastrarUsuario(repository, hasher)


def get_autenticar_usuario(
    repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> AutenticarUsuario:
    return AutenticarUsuario(repository, hasher, token_service)


def get_usuario_atual(
    credenciais: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
) -> Usuario:
    if not credenciais or credenciais.scheme.casefold() != "bearer":
        raise _erro_nao_autenticado()

    try:
        usuario_id = token_service.obter_usuario_id(credenciais.credentials)
        return ObterUsuarioAtual(repository).executar(usuario_id)
    except (
        TokenInvalidoError,
        UsuarioNaoEncontradoError,
        UsuarioInativoError,
    ) as erro:
        raise _erro_nao_autenticado() from erro


def _erro_nao_autenticado() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de acesso inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
