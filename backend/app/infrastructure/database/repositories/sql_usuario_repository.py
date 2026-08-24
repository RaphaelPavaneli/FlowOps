from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.exceptions.autenticacao import EmailJaCadastradoError
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.database.models.usuario_model import UsuarioModel


class SqlUsuarioRepository(UsuarioRepository):
    """Persistência de usuários utilizando SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def buscar_por_email(self, email: str) -> Usuario | None:
        modelo = self._session.scalar(
            select(UsuarioModel).where(UsuarioModel.email == email)
        )
        return self._para_entidade(modelo) if modelo else None

    def buscar_por_id(self, usuario_id: UUID) -> Usuario | None:
        modelo = self._session.get(UsuarioModel, usuario_id)
        return self._para_entidade(modelo) if modelo else None

    def listar(self, offset: int, limite: int) -> list[Usuario]:
        modelos = self._session.scalars(
            select(UsuarioModel)
            .order_by(UsuarioModel.criado_em.desc(), UsuarioModel.id)
            .offset(offset)
            .limit(limite)
        ).all()
        return [self._para_entidade(modelo) for modelo in modelos]

    def contar(self) -> int:
        return self._session.scalar(
            select(func.count()).select_from(UsuarioModel)
        ) or 0

    def salvar(self, usuario: Usuario) -> Usuario:
        modelo = UsuarioModel(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=usuario.senha_hash,
            perfil_acesso=usuario.perfil_acesso.value,
            equipe_id=usuario.equipe_id,
            ativo=usuario.ativo,
            criado_em=usuario.criado_em,
            atualizado_em=usuario.atualizado_em,
        )
        self._session.add(modelo)

        try:
            self._session.commit()
        except IntegrityError as erro:
            self._session.rollback()
            raise EmailJaCadastradoError from erro

        self._session.refresh(modelo)
        return self._para_entidade(modelo)

    def atualizar(self, usuario: Usuario) -> Usuario | None:
        modelo = self._session.get(UsuarioModel, usuario.id)
        if modelo is None:
            return None

        modelo.nome = usuario.nome
        modelo.email = usuario.email
        modelo.senha_hash = usuario.senha_hash
        modelo.perfil_acesso = usuario.perfil_acesso.value
        modelo.equipe_id = usuario.equipe_id
        modelo.ativo = usuario.ativo
        modelo.atualizado_em = usuario.atualizado_em
        self._session.commit()
        self._session.refresh(modelo)
        return self._para_entidade(modelo)

    @staticmethod
    def _para_entidade(modelo: UsuarioModel) -> Usuario:
        return Usuario(
            id=modelo.id,
            nome=modelo.nome,
            email=modelo.email,
            senha_hash=modelo.senha_hash,
            perfil_acesso=PerfilAcesso(modelo.perfil_acesso),
            equipe_id=modelo.equipe_id,
            ativo=modelo.ativo,
            criado_em=modelo.criado_em,
            atualizado_em=modelo.atualizado_em,
        )
