from dataclasses import dataclass
from uuid import UUID

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.automacoes import AutomacaoNaoEncontradaError
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


@dataclass(frozen=True, slots=True)
class ResultadoListaExecucoes:
    execucoes: list[Execucao]
    pagina: int
    itens_por_pagina: int
    total: int


class ListarExecucoes:
    """Lista o histórico de uma automação pertencente à equipe atual."""

    def __init__(
        self,
        automacao_repository: AutomacaoRepository,
        equipe_repository: EquipeRepository,
        execucao_repository: ExecucaoRepository,
    ) -> None:
        self._automacao_repository = automacao_repository
        self._equipe_repository = equipe_repository
        self._execucao_repository = execucao_repository

    def executar(
        self,
        usuario: Usuario,
        automacao_id: UUID,
        pagina: int,
        itens_por_pagina: int,
    ) -> ResultadoListaExecucoes:
        equipe = obter_equipe_ativa_do_usuario(
            usuario,
            self._equipe_repository,
        )
        automacao = self._automacao_repository.buscar_por_id_e_equipe(
            automacao_id,
            equipe.id,
        )
        if automacao is None:
            raise AutomacaoNaoEncontradaError

        offset = (pagina - 1) * itens_por_pagina
        return ResultadoListaExecucoes(
            execucoes=(
                self._execucao_repository.listar_por_automacao_e_equipe(
                    automacao.id,
                    equipe.id,
                    offset,
                    itens_por_pagina,
                )
            ),
            pagina=pagina,
            itens_por_pagina=itens_por_pagina,
            total=(
                self._execucao_repository.contar_por_automacao_e_equipe(
                    automacao.id,
                    equipe.id,
                )
            ),
        )
