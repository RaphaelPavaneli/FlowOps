import logging
from datetime import datetime, timezone
from uuid import UUID

from app.application.services.executor_automacao import (
    ExecucaoCanceladaError,
    ExecutorAutomacao,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_INESPERADA,
)
from app.domain.entities.automacao import Automacao
from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.repositories.execucao_repository import ExecucaoRepository


logger = logging.getLogger(__name__)


class ProcessarExecucao:
    """Executa a ação e persiste o resultado sem reutilizar a sessão HTTP."""

    def __init__(
        self,
        execucao_repository: ExecucaoRepository,
        executor_automacao: ExecutorAutomacao,
    ) -> None:
        self._execucao_repository = execucao_repository
        self._executor_automacao = executor_automacao

    def executar(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
        automacao: Automacao,
    ) -> None:
        try:
            execucao = self._execucao_repository.buscar_por_id_e_equipe(
                execucao_id,
                equipe_id,
            )
            if execucao is None:
                return

            execucao.iniciar(datetime.now(timezone.utc))
            execucao = self._execucao_repository.atualizar_se_status(
                execucao,
                frozenset({StatusExecucao.PENDENTE}),
            )
            if execucao is None:
                return

            logger.info(
                "Processamento de automação iniciado.",
                extra={
                    "automacao_id": str(automacao.id),
                    "execucao_id": str(execucao_id),
                },
            )
            try:
                self._executor_automacao.executar(execucao_id, automacao)
            except ExecucaoCanceladaError:
                logger.info(
                    "Processamento de automação cancelado.",
                    extra={
                        "automacao_id": str(automacao.id),
                        "execucao_id": str(execucao_id),
                    },
                )
                return
            except FalhaControladaAutomacaoError as erro:
                if self._registrar_falha(execucao, str(erro)):
                    logger.info(
                        "Processamento de automação finalizado com falha controlada.",
                        extra={
                            "automacao_id": str(automacao.id),
                            "execucao_id": str(execucao_id),
                        },
                    )
            except Exception:
                logger.exception(
                    "Falha inesperada ao executar automação.",
                    extra={
                        "automacao_id": str(automacao.id),
                        "execucao_id": str(execucao_id),
                    },
                )
                self._registrar_falha(
                    execucao,
                    MENSAGEM_FALHA_INESPERADA,
                )
            else:
                execucao.concluir(datetime.now(timezone.utc))
                atualizada = self._execucao_repository.atualizar_se_status(
                    execucao,
                    frozenset({StatusExecucao.PROCESSANDO}),
                )
                if atualizada is not None:
                    logger.info(
                        "Processamento de automação concluído.",
                        extra={
                            "automacao_id": str(automacao.id),
                            "execucao_id": str(execucao_id),
                        },
                    )
        finally:
            self._executor_automacao.liberar(execucao_id)

    def _registrar_falha(
        self,
        execucao: Execucao,
        mensagem: str,
    ) -> bool:
        execucao.falhar(mensagem, datetime.now(timezone.utc))
        return self._execucao_repository.atualizar_se_status(
            execucao,
            frozenset({StatusExecucao.PROCESSANDO}),
        ) is not None
