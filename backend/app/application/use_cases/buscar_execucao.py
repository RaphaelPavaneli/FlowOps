from uuid import UUID

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.execucoes import ExecucaoNaoEncontradaError
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


class BuscarExecucao:
    """Consulta uma execução sem ultrapassar a fronteira da equipe atual."""

    def __init__(
        self,
        equipe_repository: EquipeRepository,
        execucao_repository: ExecucaoRepository,
    ) -> None:
        self._equipe_repository = equipe_repository
        self._execucao_repository = execucao_repository

    def executar(self, usuario: Usuario, execucao_id: UUID) -> Execucao:
        equipe = obter_equipe_ativa_do_usuario(
            usuario,
            self._equipe_repository,
        )
        execucao = self._execucao_repository.buscar_por_id_e_equipe(
            execucao_id,
            equipe.id,
        )
        if execucao is None:
            raise ExecucaoNaoEncontradaError
        return execucao
