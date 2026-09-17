from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.execucoes import (
    MensagemFalhaExecucaoObrigatoriaError,
    TransicaoStatusExecucaoInvalidaError,
)


TRANSICOES_PERMITIDAS: dict[StatusExecucao, frozenset[StatusExecucao]] = {
    StatusExecucao.PENDENTE: frozenset(
        {
            StatusExecucao.PROCESSANDO,
            StatusExecucao.FALHOU,
        }
    ),
    StatusExecucao.PROCESSANDO: frozenset(
        {
            StatusExecucao.CONCLUIDA,
            StatusExecucao.FALHOU,
        }
    ),
}


@dataclass(slots=True)
class Execucao:
    """Execução rastreável de uma automação pertencente a uma equipe."""

    id: UUID
    automacao_id: UUID
    equipe_id: UUID
    solicitada_por_usuario_id: UUID
    status: StatusExecucao
    mensagem_erro: str | None
    criada_em: datetime
    iniciada_em: datetime | None
    finalizada_em: datetime | None
    atualizada_em: datetime

    def iniciar(self, momento: datetime) -> None:
        """Inicia o processamento de uma execução pendente."""
        self._garantir_transicao(StatusExecucao.PROCESSANDO)
        self.status = StatusExecucao.PROCESSANDO
        self.iniciada_em = momento
        self.atualizada_em = momento

    def concluir(self, momento: datetime) -> None:
        """Conclui uma execução que está em processamento."""
        self._garantir_transicao(StatusExecucao.CONCLUIDA)
        self.status = StatusExecucao.CONCLUIDA
        self.mensagem_erro = None
        self.finalizada_em = momento
        self.atualizada_em = momento

    def falhar(self, mensagem: str, momento: datetime) -> None:
        """Registra uma falha antes ou durante o processamento."""
        mensagem_limpa = " ".join(mensagem.split())
        if not mensagem_limpa:
            raise MensagemFalhaExecucaoObrigatoriaError

        self._garantir_transicao(StatusExecucao.FALHOU)
        self.status = StatusExecucao.FALHOU
        self.mensagem_erro = mensagem_limpa
        self.finalizada_em = momento
        self.atualizada_em = momento

    def _garantir_transicao(self, status_destino: StatusExecucao) -> None:
        destinos_permitidos = TRANSICOES_PERMITIDAS.get(
            self.status,
            frozenset(),
        )
        if status_destino not in destinos_permitidos:
            raise TransicaoStatusExecucaoInvalidaError(
                self.status,
                status_destino,
            )
