from dataclasses import dataclass

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.automacao import Automacao
from app.domain.entities.usuario import Usuario
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository


@dataclass(frozen=True, slots=True)
class ResultadoListaAutomacoes:
    automacoes: list[Automacao]
    pagina: int
    itens_por_pagina: int
    total: int


class ListarAutomacoes:
    """Lista as automações compartilhadas pela equipe do usuário atual."""

    def __init__(
        self,
        automacao_repository: AutomacaoRepository,
        equipe_repository: EquipeRepository,
    ) -> None:
        self._automacao_repository = automacao_repository
        self._equipe_repository = equipe_repository

    def executar(
        self,
        usuario: Usuario,
        pagina: int,
        itens_por_pagina: int,
    ) -> ResultadoListaAutomacoes:
        equipe = obter_equipe_ativa_do_usuario(
            usuario,
            self._equipe_repository,
        )
        offset = (pagina - 1) * itens_por_pagina
        return ResultadoListaAutomacoes(
            automacoes=self._automacao_repository.listar_por_equipe(
                equipe.id,
                offset,
                itens_por_pagina,
            ),
            pagina=pagina,
            itens_por_pagina=itens_por_pagina,
            total=self._automacao_repository.contar_por_equipe(equipe.id),
        )
