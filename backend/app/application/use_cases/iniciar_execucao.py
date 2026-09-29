import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.application.services.executor_automacao import (
    ExecutorAutomacao,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_INESPERADA,
)
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.automacoes import AutomacaoNaoEncontradaError
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


logger = logging.getLogger(__name__)


class IniciarExecucao:
    """Cria o registro rastreável de uma execução manual."""

    def __init__(
        self,
        automacao_repository: AutomacaoRepository,
        equipe_repository: EquipeRepository,
        execucao_repository: ExecucaoRepository,
        executor_automacao: ExecutorAutomacao,
    ) -> None:
        self._automacao_repository = automacao_repository
        self._equipe_repository = equipe_repository
        self._execucao_repository = execucao_repository
        self._executor_automacao = executor_automacao

    def executar(
        self,
        usuario: Usuario,
        automacao_id: UUID,
    ) -> Execucao:
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

        automacao.garantir_disponivel_para_execucao()
        agora = datetime.now(timezone.utc)
        execucao = Execucao(
            id=uuid4(),
            automacao_id=automacao.id,
            equipe_id=equipe.id,
            solicitada_por_usuario_id=usuario.id,
            status=StatusExecucao.PENDENTE,
            mensagem_erro=None,
            criada_em=agora,
            iniciada_em=None,
            finalizada_em=None,
            atualizada_em=agora,
        )
        execucao = self._execucao_repository.salvar(execucao)

        execucao.iniciar(datetime.now(timezone.utc))
        execucao = self._atualizar(execucao)

        try:
            self._executor_automacao.executar(automacao)
        except FalhaControladaAutomacaoError as erro:
            execucao.falhar(str(erro), datetime.now(timezone.utc))
        except Exception:
            logger.exception(
                "Falha inesperada ao executar automação.",
                extra={
                    "automacao_id": str(automacao.id),
                    "execucao_id": str(execucao.id),
                },
            )
            execucao.falhar(
                MENSAGEM_FALHA_INESPERADA,
                datetime.now(timezone.utc),
            )
        else:
            execucao.concluir(datetime.now(timezone.utc))

        return self._atualizar(execucao)

    def _atualizar(self, execucao: Execucao) -> Execucao:
        execucao_atualizada = self._execucao_repository.atualizar(execucao)
        if execucao_atualizada is None:
            raise RuntimeError(
                "A execução criada não foi encontrada para atualização."
            )
        return execucao_atualizada
