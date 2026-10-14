from datetime import datetime, timezone

from app.application.services.executor_automacao import (
    MENSAGEM_EXECUCAO_INTERROMPIDA,
)
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.repositories.execucao_repository import ExecucaoRepository


class RecuperarExecucoesInterrompidas:
    """Finaliza execuções órfãs encontradas ao iniciar uma instância única."""

    def __init__(self, execucao_repository: ExecucaoRepository) -> None:
        self._execucao_repository = execucao_repository

    def executar(self) -> int:
        recuperadas = 0
        for execucao in self._execucao_repository.listar_ativas():
            status_anterior = execucao.status
            execucao.falhar(
                MENSAGEM_EXECUCAO_INTERROMPIDA,
                datetime.now(timezone.utc),
            )
            if self._execucao_repository.atualizar_se_status(
                execucao,
                frozenset({status_anterior}),
            ) is not None:
                recuperadas += 1
        return recuperadas
