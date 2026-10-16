from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

from app.application.use_cases.listar_automacoes import ListarAutomacoes
from app.domain.entities.automacao import Automacao
from app.domain.entities.equipe import Equipe
from app.domain.entities.execucao import Execucao
from app.domain.entities.usuario import Usuario
from app.domain.enums.perfil_acesso import PerfilAcesso
from app.domain.enums.resultado_teste_controlado import ResultadoTesteControlado
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository
from app.domain.repositories.execucao_repository import ExecucaoRepository
from app.domain.value_objects.configuracao_teste_controlado import (
    ConfiguracaoTesteControlado,
)


MOMENTO = datetime(2026, 10, 14, 12, tzinfo=timezone.utc)


def test_listagem_associa_ultima_execucao_sem_alterar_entidade_automacao() -> None:
    equipe_id = uuid4()
    usuario_id = uuid4()
    automacao_id = uuid4()
    equipe = Equipe(
        id=equipe_id,
        nome="Equipe",
        ativa=True,
        criada_em=MOMENTO,
        atualizada_em=MOMENTO,
    )
    usuario = Usuario(
        id=usuario_id,
        nome="Usuário",
        email="usuario@email.com",
        senha_hash="hash",
        perfil_acesso=PerfilAcesso.USUARIO,
        equipe_id=equipe_id,
        ativo=True,
        criado_em=MOMENTO,
        atualizado_em=MOMENTO,
    )
    automacao = Automacao(
        id=automacao_id,
        equipe_id=equipe_id,
        criada_por_usuario_id=usuario_id,
        nome="Automação",
        nome_normalizado="automação",
        descricao=None,
        tipo_acao=TipoAcaoAutomacao.TESTE_CONTROLADO,
        configuracao_acao=ConfiguracaoTesteControlado(
            resultado=ResultadoTesteControlado.SUCESSO
        ),
        status=StatusAutomacao.ATIVA,
        criada_em=MOMENTO,
        atualizada_em=MOMENTO,
    )
    execucao = Execucao(
        id=uuid4(),
        automacao_id=automacao_id,
        equipe_id=equipe_id,
        solicitada_por_usuario_id=usuario_id,
        status=StatusExecucao.CONCLUIDA,
        mensagem_erro=None,
        criada_em=MOMENTO,
        iniciada_em=MOMENTO,
        finalizada_em=MOMENTO,
        atualizada_em=MOMENTO,
    )
    automacao_repository = Mock(spec=AutomacaoRepository)
    equipe_repository = Mock(spec=EquipeRepository)
    execucao_repository = Mock(spec=ExecucaoRepository)
    equipe_repository.buscar_por_id.return_value = equipe
    automacao_repository.listar_por_equipe.return_value = [automacao]
    automacao_repository.contar_por_status_e_equipe.return_value = {
        StatusAutomacao.ATIVA: 1,
        StatusAutomacao.PAUSADA: 2,
    }
    execucao_repository.buscar_ultimas_por_automacoes_e_equipe.return_value = {
        automacao_id: execucao
    }
    caso_de_uso = ListarAutomacoes(
        automacao_repository,
        equipe_repository,
        execucao_repository,
    )

    resultado = caso_de_uso.executar(usuario, pagina=1, itens_por_pagina=20)

    assert resultado.automacoes[0].automacao is automacao
    assert resultado.automacoes[0].ultima_execucao is execucao
    assert resultado.total == 3
    assert resultado.resumo.total == 3
    assert resultado.resumo.ativas == 1
    assert resultado.resumo.pausadas == 2
    assert resultado.resumo.rascunhos == 0
    automacao_repository.contar_por_status_e_equipe.assert_called_once_with(
        equipe_id
    )
    buscar_ultimas = (
        execucao_repository.buscar_ultimas_por_automacoes_e_equipe
    )
    buscar_ultimas.assert_called_once_with(
        [automacao_id], equipe_id
    )
