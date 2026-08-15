from dataclasses import dataclass

from app.application.services.password_hasher import PasswordHasher
from app.application.services.token_service import TokenService
from app.domain.exceptions.autenticacao import CredenciaisInvalidasError
from app.domain.repositories.usuario_repository import UsuarioRepository


@dataclass(frozen=True, slots=True)
class ResultadoAutenticacao:
    access_token: str
    token_type: str
    expires_in: int


class AutenticarUsuario:
    """Valida as credenciais e emite um access token."""

    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def executar(self, email: str, senha: str) -> ResultadoAutenticacao:
        usuario = self._usuario_repository.buscar_por_email(
            email.strip().casefold()
        )
        senha_valida = self._password_hasher.verificar(
            senha,
            usuario.senha_hash if usuario else None,
        )

        if not usuario or not senha_valida or not usuario.ativo:
            raise CredenciaisInvalidasError

        dados_token = self._token_service.criar_token_acesso(
            usuario.id,
            usuario.perfil_acesso,
        )
        return ResultadoAutenticacao(
            access_token=dados_token.token,
            token_type="bearer",
            expires_in=dados_token.expira_em_segundos,
        )
