from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.automacao import Automacao
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository


@dataclass(frozen=True, slots=True)
class AutomacaoListada:
    automacao: Automacao
    ultima_execucao: Execucao | None


@dataclass(frozen=True, slots=True)
class ResumoAutomacoes:
    total: int
    ativas: int
    pausadas: int
    rascunhos: int


@dataclass(frozen=True, slots=True)
class AlertaFalhaAutomacao:
    automacao_id: UUID
    automacao_nome: str
    execucao_id: UUID
    ocorrida_em: datetime


@dataclass(frozen=True, slots=True)
class ResultadoListaAutomacoes:
    automacoes: list[AutomacaoListada]
    pagina: int
    itens_por_pagina: int
    total: int
    resumo: ResumoAutomacoes
    alerta_falha: AlertaFalhaAutomacao | None


class ListarAutomacoes:
    """Lista as automações compartilhadas pela equipe do usuário atual."""

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
        pagina: int,
        itens_por_pagina: int,
        busca_nome: str | None = None,
        status: list[StatusAutomacao] | None = None,
    ) -> ResultadoListaAutomacoes:
        equipe = obter_equipe_ativa_do_usuario(
            usuario,
            self._equipe_repository,
        )
        busca_nome_normalizado = (
            " ".join(busca_nome.split()).casefold()
            if busca_nome and busca_nome.strip()
            else None
        )
        status_selecionados = frozenset(status or ())
        offset = (pagina - 1) * itens_por_pagina
        automacoes = self._automacao_repository.listar_por_equipe(
            equipe.id,
            offset,
            itens_por_pagina,
            busca_nome_normalizado,
            status_selecionados,
        )
        ultimas_execucoes = (
            self._execucao_repository.buscar_ultimas_por_automacoes_e_equipe(
                [automacao.id for automacao in automacoes],
                equipe.id,
            )
        )
        contagens = self._automacao_repository.contar_por_status_e_equipe(
            equipe.id
        )
        resumo = ResumoAutomacoes(
            total=sum(contagens.values()),
            ativas=contagens.get(StatusAutomacao.ATIVA, 0),
            pausadas=contagens.get(StatusAutomacao.PAUSADA, 0),
            rascunhos=contagens.get(StatusAutomacao.RASCUNHO, 0),
        )
        execucao_com_falha = (
            self._execucao_repository
            .buscar_falha_mais_recente_entre_ultimas_por_equipe(equipe.id)
        )
        automacao_com_falha = (
            self._automacao_repository.buscar_por_id_e_equipe(
                execucao_com_falha.automacao_id,
                equipe.id,
            )
            if execucao_com_falha
            else None
        )
        alerta_falha = (
            AlertaFalhaAutomacao(
                automacao_id=automacao_com_falha.id,
                automacao_nome=automacao_com_falha.nome,
                execucao_id=execucao_com_falha.id,
                ocorrida_em=(
                    execucao_com_falha.finalizada_em
                    or execucao_com_falha.atualizada_em
                ),
            )
            if execucao_com_falha and automacao_com_falha
            else None
        )
        total_filtrado = (
            self._automacao_repository.contar_filtradas_por_equipe(
                equipe.id,
                busca_nome_normalizado,
                status_selecionados,
            )
        )
        return ResultadoListaAutomacoes(
            automacoes=[
                AutomacaoListada(
                    automacao=automacao,
                    ultima_execucao=ultimas_execucoes.get(automacao.id),
                )
                for automacao in automacoes
            ],
            pagina=pagina,
            itens_por_pagina=itens_por_pagina,
            total=total_filtrado,
            resumo=resumo,
            alerta_falha=alerta_falha,
        )
