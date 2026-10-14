import logging
from datetime import datetime, timezone
from uuid import UUID

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.application.services.despachante_execucao import (
    DespachanteExecucao,
)
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.execucoes import (
    ExecucaoIndisponivelParaCancelamentoError,
    ExecucaoNaoEncontradaError,
)
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


STATUS_ATIVOS = frozenset(
    {StatusExecucao.PENDENTE, StatusExecucao.PROCESSANDO}
)

logger = logging.getLogger(__name__)


class CancelarExecucao:
    """Cancela de forma atômica uma execução da equipe ativa."""

    def __init__(
        self,
        equipe_repository: EquipeRepository,
        execucao_repository: ExecucaoRepository,
        despachante_execucao: DespachanteExecucao,
    ) -> None:
        self._equipe_repository = equipe_repository
        self._execucao_repository = execucao_repository
        self._despachante_execucao = despachante_execucao

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
        if execucao.status not in STATUS_ATIVOS:
            raise ExecucaoIndisponivelParaCancelamentoError

        status_anterior = execucao.status
        execucao.cancelar(datetime.now(timezone.utc))
        execucao_atualizada = self._execucao_repository.atualizar_se_status(
            execucao,
            frozenset({status_anterior}),
        )
        if execucao_atualizada is None:
            raise ExecucaoIndisponivelParaCancelamentoError

        processo_sinalizado = self._despachante_execucao.cancelar(execucao_id)
        logger.info(
            "Cancelamento de execução registrado.",
            extra={
                "automacao_id": str(execucao.automacao_id),
                "execucao_id": str(execucao_id),
                "processo_sinalizado": processo_sinalizado,
            },
        )
        return execucao_atualizada
