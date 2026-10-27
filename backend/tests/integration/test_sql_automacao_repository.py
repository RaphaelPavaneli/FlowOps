from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.orm import Session, sessionmaker

from app.domain.enums.status_automacao import StatusAutomacao
from app.infrastructure.database.models.automacao_model import AutomacaoModel
from app.infrastructure.database.repositories.sql_automacao_repository import (
    SqlAutomacaoRepository,
)


MOMENTO = datetime(2026, 10, 20, 12, tzinfo=timezone.utc)


def criar_modelo(
    equipe_id: UUID,
    nome: str,
    status: StatusAutomacao,
) -> AutomacaoModel:
    return AutomacaoModel(
        id=uuid4(),
        equipe_id=equipe_id,
        criada_por_usuario_id=uuid4(),
        nome=nome,
        nome_normalizado=nome.casefold(),
        descricao=None,
        tipo_acao="teste_controlado",
        configuracao_acao='{"resultado": "sucesso"}',
        status=status.value,
        criada_em=MOMENTO,
        atualizada_em=MOMENTO,
    )


def test_listagem_filtra_nome_e_status_sem_vazar_entre_equipes(
    session_factory: sessionmaker[Session],
) -> None:
    equipe_id = uuid4()
    outra_equipe_id = uuid4()
    with session_factory() as session:
        session.add_all(
            [
                criar_modelo(
                    equipe_id,
                    "Enviar relatório diário",
                    StatusAutomacao.RASCUNHO,
                ),
                criar_modelo(
                    equipe_id,
                    "Relatório mensal",
                    StatusAutomacao.PAUSADA,
                ),
                criar_modelo(
                    equipe_id,
                    "Sincronizar pedidos",
                    StatusAutomacao.ATIVA,
                ),
                criar_modelo(
                    outra_equipe_id,
                    "Relatório externo",
                    StatusAutomacao.PAUSADA,
                ),
            ]
        )
        session.commit()

        repository = SqlAutomacaoRepository(session)
        status = frozenset(
            {StatusAutomacao.RASCUNHO, StatusAutomacao.PAUSADA}
        )

        automacoes = repository.listar_por_equipe(
            equipe_id,
            offset=0,
            limite=1,
            busca_nome_normalizado="relatório",
            status=status,
        )
        total = repository.contar_filtradas_por_equipe(
            equipe_id,
            busca_nome_normalizado="relatório",
            status=status,
        )
        resumo = repository.contar_por_status_e_equipe(equipe_id)

    assert len(automacoes) == 1
    assert automacoes[0].equipe_id == equipe_id
    assert "relatório" in automacoes[0].nome_normalizado
    assert automacoes[0].status in status
    assert total == 2
    assert resumo == {
        StatusAutomacao.ATIVA: 1,
        StatusAutomacao.PAUSADA: 1,
        StatusAutomacao.RASCUNHO: 1,
    }


def test_busca_trata_caracteres_curinga_como_texto(
    session_factory: sessionmaker[Session],
) -> None:
    equipe_id = uuid4()
    with session_factory() as session:
        session.add_all(
            [
                criar_modelo(
                    equipe_id,
                    "Processo 100% concluído",
                    StatusAutomacao.ATIVA,
                ),
                criar_modelo(
                    equipe_id,
                    "Processo comum",
                    StatusAutomacao.ATIVA,
                ),
            ]
        )
        session.commit()

        repository = SqlAutomacaoRepository(session)
        total = repository.contar_filtradas_por_equipe(
            equipe_id,
            busca_nome_normalizado="%",
        )

    assert total == 1
