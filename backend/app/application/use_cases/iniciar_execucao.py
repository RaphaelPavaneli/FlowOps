from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.automacoes import AutomacaoNaoEncontradaError
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


class IniciarExecucao:
    """Cria o registro rastreável de uma execução manual."""

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
        return self._execucao_repository.salvar(execucao)
