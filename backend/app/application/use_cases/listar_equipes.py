from dataclasses import dataclass

from app.domain.entities.equipe import Equipe
from app.domain.repositories.equipe_repository import EquipeRepository


@dataclass(frozen=True, slots=True)
class ResultadoListaEquipes:
    equipes: list[Equipe]
    pagina: int
    itens_por_pagina: int
    total: int


class ListarEquipes:
    """Lista equipes com paginação estável."""

    def __init__(self, equipe_repository: EquipeRepository) -> None:
        self._equipe_repository = equipe_repository

    def executar(self, pagina: int, itens_por_pagina: int) -> ResultadoListaEquipes:
        offset = (pagina - 1) * itens_por_pagina
        return ResultadoListaEquipes(
            equipes=self._equipe_repository.listar(offset, itens_por_pagina),
            pagina=pagina,
            itens_por_pagina=itens_por_pagina,
            total=self._equipe_repository.contar(),
        )
