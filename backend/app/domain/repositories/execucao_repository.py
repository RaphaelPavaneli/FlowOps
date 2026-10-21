from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao


class ExecucaoRepository(ABC):
    """Contrato de persistência das execuções de automação."""

    @abstractmethod
    def salvar(self, execucao: Execucao) -> Execucao:
        """Persiste uma nova execução."""

    @abstractmethod
    def atualizar(self, execucao: Execucao) -> Execucao | None:
        """Atualiza uma execução existente."""

    @abstractmethod
    def atualizar_se_status(
        self,
        execucao: Execucao,
        status_esperados: frozenset[StatusExecucao],
    ) -> Execucao | None:
        """Atualiza somente quando o estado persistido ainda é o esperado."""

    @abstractmethod
    def existe_ativa_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
    ) -> bool:
        """Informa se a automação já possui execução ativa."""

    @abstractmethod
    def listar_ativas(self) -> list[Execucao]:
        """Lista execuções ativas para recuperação interna do serviço."""

    @abstractmethod
    def buscar_por_id_e_equipe(
        self,
        execucao_id: UUID,
        equipe_id: UUID,
    ) -> Execucao | None:
        """Busca uma execução somente dentro da equipe informada."""

    @abstractmethod
    def listar_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
        offset: int,
        limite: int,
    ) -> list[Execucao]:
        """Lista o histórico de uma automação dentro da equipe."""

    @abstractmethod
    def buscar_ultimas_por_automacoes_e_equipe(
        self,
        automacao_ids: list[UUID],
        equipe_id: UUID,
    ) -> dict[UUID, Execucao]:
        """Busca a execução mais recente de cada automação informada."""

    @abstractmethod
    def buscar_falha_mais_recente_entre_ultimas_por_equipe(
        self,
        equipe_id: UUID,
    ) -> Execucao | None:
        """Busca a falha mais recente entre as últimas execuções da equipe."""

    @abstractmethod
    def contar_por_automacao_e_equipe(
        self,
        automacao_id: UUID,
        equipe_id: UUID,
    ) -> int:
        """Conta as execuções de uma automação dentro da equipe."""
