from datetime import datetime, timezone
from uuid import uuid4

from app.application.services.password_hasher import PasswordHasher
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.exceptions.autenticacao import EmailJaCadastradoError
from app.domain.repositories.usuario_repository import UsuarioRepository


class CadastrarUsuario:
    """Cadastra um usuário comum após validar a unicidade do e-mail."""

    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher

    def executar(self, nome: str, email: str, senha: str) -> Usuario:
        email_normalizado = email.strip().casefold()
        if self._usuario_repository.buscar_por_email(email_normalizado):
            raise EmailJaCadastradoError

        agora = datetime.now(timezone.utc)
        usuario = Usuario(
            id=uuid4(),
            nome=nome.strip(),
            email=email_normalizado,
            senha_hash=self._password_hasher.gerar_hash(senha),
            perfil_acesso=PerfilAcesso.USUARIO,
            equipe_id=None,
            ativo=True,
            criado_em=agora,
            atualizado_em=agora,
        )
        return self._usuario_repository.salvar(usuario)
