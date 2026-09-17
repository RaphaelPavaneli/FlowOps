from datetime import datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.execucao import Execucao
from app.domain.enums.status_execucao import StatusExecucao
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
) -> Execucao:
    return Execucao(
        id=execucao_id or uuid4(),
        automacao_id=automacao_id or uuid4(),
        equipe_id=equipe_id or uuid4(),
        solicitada_por_usuario_id=solicitante_id or uuid4(),
        status=StatusExecucao.PENDENTE,
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
        ),
        criar_execucao(
            execucao_id=execucao_id_3,
            automacao_id=automacao_id,
            equipe_id=equipe_id,
            criada_em=momento_recente,
        ),
        criar_execucao(
            execucao_id=UUID(int=1),
            automacao_id=automacao_id,
            equipe_id=equipe_id,
        ),
    ]
    fora_do_escopo = [
        criar_execucao(
            automacao_id=automacao_id,
            equipe_id=outra_equipe_id,
        ),
        criar_execucao(
            automacao_id=outra_automacao_id,
            equipe_id=equipe_id,
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
                automacao_id=automacao_id,
                equipe_id=outra_equipe_id,
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
