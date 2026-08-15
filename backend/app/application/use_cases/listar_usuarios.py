from dataclasses import dataclass

from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository


@dataclass(frozen=True, slots=True)
class ResultadoListaUsuarios:
    usuarios: list[Usuario]
    pagina: int
    itens_por_pagina: int
    total: int


class ListarUsuarios:
    """Lista usuários com paginação estável."""

    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self._usuario_repository = usuario_repository

    def executar(self, pagina: int, itens_por_pagina: int) -> ResultadoListaUsuarios:
        offset = (pagina - 1) * itens_por_pagina
        return ResultadoListaUsuarios(
            usuarios=self._usuario_repository.listar(offset, itens_por_pagina),
            pagina=pagina,
            itens_por_pagina=itens_por_pagina,
            total=self._usuario_repository.contar(),
        )
