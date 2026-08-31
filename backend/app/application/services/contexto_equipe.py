from app.domain.entities.equipe import Equipe
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.automacoes import (
    EquipeUsuarioIndisponivelError,
    UsuarioSemEquipeError,
)
from app.domain.repositories.equipe_repository import EquipeRepository


def obter_equipe_ativa_do_usuario(
    usuario: Usuario,
    equipe_repository: EquipeRepository,
) -> Equipe:
    """Resolve no banco a fronteira operacional do usuário autenticado."""

    if usuario.equipe_id is None:
        raise UsuarioSemEquipeError

    equipe = equipe_repository.buscar_por_id(usuario.equipe_id)
    if equipe is None or not equipe.ativa:
        raise EquipeUsuarioIndisponivelError
    return equipe
