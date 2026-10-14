from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

from app.application.services.executor_automacao import MENSAGEM_EXECUCAO_INTERROMPIDA
from app.application.use_cases.recuperar_execucoes_interrompidas import (
    RecuperarExecucoesInterrompidas,
)
from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.repositories.execucao_repository import ExecucaoRepository


def criar_execucao(status: StatusExecucao) -> Execucao:
    agora = datetime(2026, 10, 2, 12, tzinfo=timezone.utc)
    return Execucao(
        id=uuid4(),
        automacao_id=uuid4(),
        equipe_id=uuid4(),
        solicitada_por_usuario_id=uuid4(),
        status=status,
        mensagem_erro=None,
        criada_em=agora,
        iniciada_em=agora if status is StatusExecucao.PROCESSANDO else None,
        finalizada_em=None,
        atualizada_em=agora,
    )


def test_recupera_pendentes_e_processando_como_falha_de_reinicio() -> None:
    pendente = criar_execucao(StatusExecucao.PENDENTE)
    processando = criar_execucao(StatusExecucao.PROCESSANDO)
    repositorio = Mock(spec=ExecucaoRepository)
    repositorio.listar_ativas.return_value = [pendente, processando]
    repositorio.atualizar_se_status.side_effect = lambda execucao, _: execucao

    quantidade = RecuperarExecucoesInterrompidas(repositorio).executar()

    assert quantidade == 2
    assert pendente.status is StatusExecucao.FALHOU
    assert processando.status is StatusExecucao.FALHOU
    assert pendente.mensagem_erro == MENSAGEM_EXECUCAO_INTERROMPIDA
    assert processando.mensagem_erro == MENSAGEM_EXECUCAO_INTERROMPIDA
