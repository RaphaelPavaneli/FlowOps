from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao
from app.domain.exceptions.execucoes import ExecucaoEmAndamentoError
from app.infrastructure.database.repositories.sql_execucao_repository import (
    SqlExecucaoRepository,
)


MOMENTO_CRIACAO = datetime(2026, 9, 16, 12)
MOMENTO_INICIO = MOMENTO_CRIACAO + timedelta(minutes=1)


def criar_execucao(
    *,
    execucao_id: UUID | None = None,
    automacao_id: UUID | None = None,
    equipe_id: UUID | None = None,
    solicitante_id: UUID | None = None,
    criada_em: datetime = MOMENTO_CRIACAO,
    status: StatusExecucao = StatusExecucao.PENDENTE,
) -> Execucao:
    return Execucao(
        id=execucao_id or uuid4(),
        automacao_id=automacao_id or uuid4(),
        equipe_id=equipe_id or uuid4(),
        solicitada_por_usuario_id=solicitante_id or uuid4(),
        status=status,
        mensagem_erro=None,
        criada_em=criada_em,
        iniciada_em=None,
        finalizada_em=None,
        atualizada_em=criada_em,
    )


def test_salvar_e_recuperar_execucao(
    session_factory: sessionmaker[Session],
) -> None:
    execucao = criar_execucao()

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)

        salva = repositorio.salvar(execucao)
        recuperada = repositorio.buscar_por_id_e_equipe(
            execucao.id,
            execucao.equipe_id,
        )

    assert salva == execucao
    assert recuperada == execucao
    assert recuperada is not execucao


def test_atualizar_altera_estado_e_preserva_dados_que_identificam_execucao(
    session_factory: sessionmaker[Session],
) -> None:
    execucao = criar_execucao()

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        repositorio.salvar(execucao)
        atualizacao = Execucao(
            id=execucao.id,
            automacao_id=uuid4(),
            equipe_id=execucao.equipe_id,
            solicitada_por_usuario_id=uuid4(),
            status=StatusExecucao.PROCESSANDO,
            mensagem_erro=None,
            criada_em=MOMENTO_CRIACAO - timedelta(days=1),
            iniciada_em=MOMENTO_INICIO,
            finalizada_em=None,
            atualizada_em=MOMENTO_INICIO,
        )

        atualizada = repositorio.atualizar(atualizacao)

    assert atualizada is not None
    assert atualizada.status is StatusExecucao.PROCESSANDO
    assert atualizada.iniciada_em == MOMENTO_INICIO
    assert atualizada.atualizada_em == MOMENTO_INICIO
    assert atualizada.automacao_id == execucao.automacao_id
    assert atualizada.equipe_id == execucao.equipe_id
    assert (
        atualizada.solicitada_por_usuario_id
        == execucao.solicitada_por_usuario_id
    )
    assert atualizada.criada_em == execucao.criada_em


def test_atualizar_execucao_inexistente_retorna_none(
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)

        resultado = repositorio.atualizar(criar_execucao())

    assert resultado is None


def test_busca_e_atualizacao_nao_vazam_entre_equipes(
    session_factory: sessionmaker[Session],
) -> None:
    execucao = criar_execucao()
    outra_equipe_id = uuid4()

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        repositorio.salvar(execucao)
        encontrada = repositorio.buscar_por_id_e_equipe(
            execucao.id,
            outra_equipe_id,
        )
        atualizacao_externa = Execucao(
            id=execucao.id,
            automacao_id=execucao.automacao_id,
            equipe_id=outra_equipe_id,
            solicitada_por_usuario_id=execucao.solicitada_por_usuario_id,
            status=StatusExecucao.PROCESSANDO,
            mensagem_erro=None,
            criada_em=execucao.criada_em,
            iniciada_em=MOMENTO_INICIO,
            finalizada_em=None,
            atualizada_em=MOMENTO_INICIO,
        )
        atualizada = repositorio.atualizar(atualizacao_externa)
        original = repositorio.buscar_por_id_e_equipe(
            execucao.id,
            execucao.equipe_id,
        )

    assert encontrada is None
    assert atualizada is None
    assert original is not None
    assert original.status is StatusExecucao.PENDENTE


def test_historico_isola_equipe_automacao_e_pagina_deterministicamente(
    session_factory: sessionmaker[Session],
) -> None:
    equipe_id = uuid4()
    outra_equipe_id = uuid4()
    automacao_id = uuid4()
    outra_automacao_id = uuid4()
    momento_recente = MOMENTO_CRIACAO + timedelta(minutes=2)
    execucao_id_2 = UUID(int=2)
    execucao_id_3 = UUID(int=3)
    execucoes_esperadas = [
        criar_execucao(
            execucao_id=execucao_id_2,
            automacao_id=automacao_id,
            equipe_id=equipe_id,
            criada_em=momento_recente,
            status=StatusExecucao.CONCLUIDA,
        ),
        criar_execucao(
            execucao_id=execucao_id_3,
            automacao_id=automacao_id,
            equipe_id=equipe_id,
            criada_em=momento_recente,
            status=StatusExecucao.FALHOU,
        ),
        criar_execucao(
            execucao_id=UUID(int=1),
            automacao_id=automacao_id,
            equipe_id=equipe_id,
            status=StatusExecucao.CANCELADA,
        ),
    ]
    fora_do_escopo = [
        criar_execucao(
            automacao_id=automacao_id,
            equipe_id=outra_equipe_id,
            status=StatusExecucao.CONCLUIDA,
        ),
        criar_execucao(
            automacao_id=outra_automacao_id,
            equipe_id=equipe_id,
            status=StatusExecucao.CONCLUIDA,
        ),
    ]

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        for execucao in execucoes_esperadas + fora_do_escopo:
            repositorio.salvar(execucao)

        primeira_pagina = repositorio.listar_por_automacao_e_equipe(
            automacao_id,
            equipe_id,
            offset=0,
            limite=2,
        )
        segunda_pagina = repositorio.listar_por_automacao_e_equipe(
            automacao_id,
            equipe_id,
            offset=2,
            limite=2,
        )

    assert [item.id for item in primeira_pagina] == [
        execucao_id_2,
        execucao_id_3,
    ]
    assert [item.id for item in segunda_pagina] == [UUID(int=1)]


def test_busca_ultima_execucao_de_cada_automacao_sem_vazar_equipe(
    session_factory: sessionmaker[Session],
) -> None:
    equipe_id = uuid4()
    outra_equipe_id = uuid4()
    automacao_a_id = uuid4()
    automacao_b_id = uuid4()
    execucao_a_antiga = criar_execucao(
        automacao_id=automacao_a_id,
        equipe_id=equipe_id,
        status=StatusExecucao.CONCLUIDA,
    )
    execucao_a_recente = criar_execucao(
        automacao_id=automacao_a_id,
        equipe_id=equipe_id,
        criada_em=MOMENTO_CRIACAO + timedelta(minutes=2),
        status=StatusExecucao.FALHOU,
    )
    execucao_b = criar_execucao(
        automacao_id=automacao_b_id,
        equipe_id=equipe_id,
        status=StatusExecucao.CANCELADA,
    )
    execucao_outra_equipe = criar_execucao(
        automacao_id=automacao_a_id,
        equipe_id=outra_equipe_id,
        criada_em=MOMENTO_CRIACAO + timedelta(minutes=3),
        status=StatusExecucao.CONCLUIDA,
    )

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        for execucao in (
            execucao_a_antiga,
            execucao_a_recente,
            execucao_b,
            execucao_outra_equipe,
        ):
            repositorio.salvar(execucao)

        resultado = repositorio.buscar_ultimas_por_automacoes_e_equipe(
            [automacao_a_id, automacao_b_id, uuid4()],
            equipe_id,
        )

    assert set(resultado) == {automacao_a_id, automacao_b_id}
    assert resultado[automacao_a_id].id == execucao_a_recente.id
    assert resultado[automacao_b_id].id == execucao_b.id


def test_contagem_considera_automacao_e_equipe(
    session_factory: sessionmaker[Session],
) -> None:
    equipe_id = uuid4()
    outra_equipe_id = uuid4()
    automacao_id = uuid4()

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        repositorio.salvar(
            criar_execucao(
                automacao_id=automacao_id,
                equipe_id=equipe_id,
                status=StatusExecucao.CONCLUIDA,
            )
        )
        repositorio.salvar(
            criar_execucao(
                automacao_id=automacao_id,
                equipe_id=equipe_id,
                status=StatusExecucao.FALHOU,
            )
        )
        repositorio.salvar(
            criar_execucao(
                automacao_id=automacao_id,
                equipe_id=outra_equipe_id,
                status=StatusExecucao.CANCELADA,
            )
        )

        total = repositorio.contar_por_automacao_e_equipe(
            automacao_id,
            equipe_id,
        )
        total_inexistente = repositorio.contar_por_automacao_e_equipe(
            uuid4(),
            equipe_id,
        )

    assert total == 2
    assert total_inexistente == 0


def test_indice_impede_duas_execucoes_ativas_da_mesma_automacao(
    session_factory: sessionmaker[Session],
) -> None:
    automacao_id = uuid4()
    equipe_id = uuid4()

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        repositorio.salvar(
            criar_execucao(
                automacao_id=automacao_id,
                equipe_id=equipe_id,
            )
        )

        with pytest.raises(ExecucaoEmAndamentoError):
            repositorio.salvar(
                criar_execucao(
                    automacao_id=automacao_id,
                    equipe_id=equipe_id,
                )
            )


def test_indice_permite_historico_terminal_e_automacoes_diferentes(
    session_factory: sessionmaker[Session],
) -> None:
    automacao_id = uuid4()
    equipe_id = uuid4()

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        repositorio.salvar(
            criar_execucao(
                automacao_id=automacao_id,
                equipe_id=equipe_id,
                status=StatusExecucao.CONCLUIDA,
            )
        )
        repositorio.salvar(
            criar_execucao(
                automacao_id=automacao_id,
                equipe_id=equipe_id,
            )
        )
        repositorio.salvar(
            criar_execucao(
                automacao_id=uuid4(),
                equipe_id=equipe_id,
            )
        )


def test_atualizacao_condicional_nao_sobrescreve_estado_terminal(
    session_factory: sessionmaker[Session],
) -> None:
    execucao = criar_execucao(status=StatusExecucao.CANCELADA)
    tentativa = criar_execucao(
        execucao_id=execucao.id,
        automacao_id=execucao.automacao_id,
        equipe_id=execucao.equipe_id,
        solicitante_id=execucao.solicitada_por_usuario_id,
        status=StatusExecucao.CONCLUIDA,
    )

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        repositorio.salvar(execucao)
        resultado = repositorio.atualizar_se_status(
            tentativa,
            frozenset({StatusExecucao.PROCESSANDO}),
        )
        persistida = repositorio.buscar_por_id_e_equipe(
            execucao.id,
            execucao.equipe_id,
        )

    assert resultado is None
    assert persistida is not None
    assert persistida.status is StatusExecucao.CANCELADA
