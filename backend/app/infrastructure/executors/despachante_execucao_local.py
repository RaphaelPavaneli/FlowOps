from concurrent.futures import ThreadPoolExecutor
from uuid import UUID

from sqlalchemy.orm import Session, sessionmaker

from app.application.services.despachante_execucao import (
    DespachanteExecucao,
)
from app.application.services.executor_automacao import ExecutorAutomacao
from app.application.use_cases.processar_execucao import ProcessarExecucao
from app.domain.entities.automacao import Automacao
from app.infrastructure.database.repositories.sql_execucao_repository import (
    SqlExecucaoRepository,
)


MAXIMO_EXECUCOES_SIMULTANEAS = 4


class DespachanteExecucaoLocal(DespachanteExecucao):
    """Agenda execuções locais em threads e subprocessos independentes."""

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        executor_automacao: ExecutorAutomacao,
        max_workers: int = MAXIMO_EXECUCOES_SIMULTANEAS,
    ) -> None:
        self._session_factory = session_factory
        self._executor_automacao = executor_automacao
        self._pool = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="flowops-execucao",
        )

    def despachar(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
        automacao: Automacao,
    ) -> None:
        self._executor_automacao.preparar(execucao_id)
        try:
            self._pool.submit(
                self._processar,
                execucao_id,
                equipe_id,
                automacao,
            )
        except Exception:
            self._executor_automacao.liberar(execucao_id)
            raise

    def cancelar(self, execucao_id: UUID) -> bool:
        return self._executor_automacao.cancelar(execucao_id)

    def encerrar(self) -> None:
        self._executor_automacao.encerrar_todos()
        self._pool.shutdown(wait=True, cancel_futures=True)

    def _processar(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
        automacao: Automacao,
    ) -> None:
        with self._session_factory() as session:
            ProcessarExecucao(
                SqlExecucaoRepository(session),
                self._executor_automacao,
            ).executar(execucao_id, equipe_id, automacao)
