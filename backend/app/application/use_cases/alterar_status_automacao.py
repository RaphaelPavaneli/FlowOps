from datetime import datetime, timezone
from uuid import UUID

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.automacao import Automacao
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.automacoes import AutomacaoNaoEncontradaError
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository


class AlterarStatusAutomacao:
    """Ativa ou pausa uma automação da equipe do usuário atual."""

    def __init__(
        self,
        automacao_repository: AutomacaoRepository,
        equipe_repository: EquipeRepository,
    ) -> None:
        self._automacao_repository = automacao_repository
        self._equipe_repository = equipe_repository

    def ativar(
        self,
        usuario: Usuario,
        automacao_id: UUID,
    ) -> Automacao:
        automacao = self._buscar_automacao(usuario, automacao_id)
        automacao.ativar(datetime.now(timezone.utc))
        return self._atualizar(automacao)

    def pausar(
        self,
        usuario: Usuario,
        automacao_id: UUID,
    ) -> Automacao:
        automacao = self._buscar_automacao(usuario, automacao_id)
        automacao.pausar(datetime.now(timezone.utc))
        return self._atualizar(automacao)

    def _buscar_automacao(
        self,
        usuario: Usuario,
        automacao_id: UUID,
    ) -> Automacao:
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
        return automacao

    def _atualizar(self, automacao: Automacao) -> Automacao:
        atualizada = self._automacao_repository.atualizar(automacao)
        if atualizada is None:
            raise AutomacaoNaoEncontradaError
        return atualizada
