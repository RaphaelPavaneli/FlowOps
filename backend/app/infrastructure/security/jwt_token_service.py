from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
from jwt.exceptions import InvalidTokenError

from app.application.services.token_service import DadosTokenAcesso, TokenService
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.exceptions.autenticacao import TokenInvalidoError


class JwtTokenService(TokenService):
    """Emite e valida access tokens JWT assinados."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        issuer: str,
        audience: str,
        expire_minutes: int,
    ) -> None:
        if len(secret_key) < 32:
            raise ValueError(
                "FLOWOPS_JWT_SECRET_KEY deve possuir pelo menos 32 caracteres."
            )

        self._secret_key = secret_key
        self._algorithm = algorithm
        self._issuer = issuer
        self._audience = audience
        self._expire_minutes = expire_minutes

    def criar_token_acesso(
        self,
        usuario_id: UUID,
        perfil_acesso: PerfilAcesso,
    ) -> DadosTokenAcesso:
        agora = datetime.now(timezone.utc)
        expira_em = agora + timedelta(minutes=self._expire_minutes)
        expira_em_segundos = self._expire_minutes * 60
        payload = {
            "sub": str(usuario_id),
            "iss": self._issuer,
            "aud": self._audience,
            "iat": agora,
            "nbf": agora,
            "exp": expira_em,
            "jti": str(uuid4()),
            "type": "access",
            "perfil_acesso": perfil_acesso.value,
        }
        token = jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )
        return DadosTokenAcesso(
            token=token,
            expira_em_segundos=expira_em_segundos,
        )

    def obter_usuario_id(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                audience=self._audience,
                issuer=self._issuer,
                options={
                    "require": [
                        "sub",
                        "iss",
                        "aud",
                        "iat",
                        "nbf",
                        "exp",
                        "jti",
                        "type",
                    ]
                },
            )
            if payload["type"] != "access":
                raise TokenInvalidoError
            return UUID(payload["sub"])
        except (InvalidTokenError, KeyError, TypeError, ValueError) as erro:
            raise TokenInvalidoError from erro
