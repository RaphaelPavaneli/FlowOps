from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.models.automacao_model import AutomacaoModel
from app.infrastructure.database.models.equipe_model import EquipeModel
from app.infrastructure.database.models.execucao_model import ExecucaoModel
from app.infrastructure.database.models.usuario_model import UsuarioModel


SENHA_TESTE = "uma senha longa e segura"


def cadastrar_usuario(
    client: TestClient,
    nome: str,
    email: str,
) -> dict:
    response = client.post(
        "/api/v1/autenticacao/cadastro",
        json={"nome": nome, "email": email, "senha": SENHA_TESTE},
    )
    assert response.status_code == 201
    return response.json()


def tornar_administrador(
    session_factory: sessionmaker[Session],
    email: str,
) -> None:
    with session_factory() as session:
        usuario = session.scalar(
            select(UsuarioModel).where(UsuarioModel.email == email)
        )
        assert usuario is not None
        usuario.perfil_acesso = "administrador"
        session.commit()


def obter_token(client: TestClient, email: str) -> str:
    response = client.post(
        "/api/v1/autenticacao/login",
        json={"email": email, "senha": SENHA_TESTE},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def preparar_administrador(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> str:
    cadastrar_usuario(client, "Administrador", "admin@email.com")
    tornar_administrador(session_factory, "admin@email.com")
    return obter_token(client, "admin@email.com")


def criar_equipe(client: TestClient, admin_token: str, nome: str) -> dict:
    response = client.post(
        "/api/v1/equipes",
        json={"nome": nome},
        headers=headers(admin_token),
    )
    assert response.status_code == 201
    return response.json()


def associar_usuario(
    client: TestClient,
    admin_token: str,
    equipe_id: str,
    usuario_id: str,
) -> None:
    response = client.put(
        f"/api/v1/equipes/{equipe_id}/membros/{usuario_id}",
        headers=headers(admin_token),
    )
    assert response.status_code == 200


def preparar_usuario_com_equipe(
    client: TestClient,
    admin_token: str,
    *,
    nome: str,
    email: str,
    equipe: dict,
) -> tuple[dict, str]:
    usuario = cadastrar_usuario(client, nome, email)
    associar_usuario(client, admin_token, equipe["id"], usuario["id"])
    return usuario, obter_token(client, email)


def criar_automacao(
    client: TestClient,
    token: str,
    nome: str,
    descricao: str | None = None,
) -> dict:
    response = client.post(
        "/api/v1/automacoes",
        json={"nome": nome, "descricao": descricao},
        headers=headers(token),
    )
    assert response.status_code == 201
    return response.json()


def test_automacoes_exigem_autenticacao(client: TestClient) -> None:
    criacao = client.post(
        "/api/v1/automacoes",
        json={"nome": "Automação teste"},
    )
    listagem = client.get("/api/v1/automacoes")
    ativacao = client.post(f"/api/v1/automacoes/{uuid4()}/ativar")
    pausa = client.post(f"/api/v1/automacoes/{uuid4()}/pausar")

    assert criacao.status_code == 401
    assert listagem.status_code == 401
    assert ativacao.status_code == 401
    assert pausa.status_code == 401


def test_usuario_sem_equipe_nao_acessa_automacoes(client: TestClient) -> None:
    cadastrar_usuario(client, "Usuário sem equipe", "sem.equipe@email.com")
    token = obter_token(client, "sem.equipe@email.com")

    criacao = client.post(
        "/api/v1/automacoes",
        json={"nome": "Automação teste"},
        headers=headers(token),
    )
    listagem = client.get("/api/v1/automacoes", headers=headers(token))

    assert criacao.status_code == 409
    assert listagem.status_code == 409
    assert criacao.json()["detail"] == (
        "O usuário precisa estar associado a uma equipe."
    )


def test_usuario_cria_automacao_em_rascunho_na_propria_equipe(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    usuario, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário criador",
        email="criador@email.com",
        equipe=equipe,
    )

    response = client.post(
        "/api/v1/automacoes",
        json={
            "nome": "  Enviar   relatório diário  ",
            "descricao": "  Relatório financeiro  ",
        },
        headers=headers(token),
    )

    assert response.status_code == 201
    dados = response.json()
    assert dados["equipe_id"] == equipe["id"]
    assert dados["criada_por_usuario_id"] == usuario["id"]
    assert dados["nome"] == "Enviar relatório diário"
    assert dados["descricao"] == "Relatório financeiro"
    assert dados["status"] == "rascunho"


def test_cliente_nao_pode_escolher_equipe_criador_ou_status(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    usuario, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário criador",
        email="criador@email.com",
        equipe=equipe,
    )

    response = client.post(
        "/api/v1/automacoes",
        json={
            "nome": "Automação forjada",
            "equipe_id": equipe["id"],
            "criada_por_usuario_id": usuario["id"],
            "status": "ativa",
        },
        headers=headers(token),
    )

    assert response.status_code == 422


def test_nome_duplicado_na_mesma_equipe_retorna_409(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário criador",
        email="criador@email.com",
        equipe=equipe,
    )
    criar_automacao(client, token, "Enviar Relatório")

    response = client.post(
        "/api/v1/automacoes",
        json={"nome": "  enviar   relatório  "},
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Já existe uma automação com este nome na equipe."
    )


def test_mesmo_nome_e_permitido_em_equipes_diferentes(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe_a = criar_equipe(client, admin_token, "Equipe A")
    equipe_b = criar_equipe(client, admin_token, "Equipe B")
    _, token_a = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário A",
        email="usuario.a@email.com",
        equipe=equipe_a,
    )
    _, token_b = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário B",
        email="usuario.b@email.com",
        equipe=equipe_b,
    )

    primeira = client.post(
        "/api/v1/automacoes",
        json={"nome": "Automação compartilhada"},
        headers=headers(token_a),
    )
    segunda = client.post(
        "/api/v1/automacoes",
        json={"nome": "Automação compartilhada"},
        headers=headers(token_b),
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201


def test_membros_compartilham_automacoes_sem_vazar_entre_equipes(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe_a = criar_equipe(client, admin_token, "Equipe A")
    equipe_b = criar_equipe(client, admin_token, "Equipe B")
    _, token_criador = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Criador",
        email="criador@email.com",
        equipe=equipe_a,
    )
    _, token_colega = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Colega",
        email="colega@email.com",
        equipe=equipe_a,
    )
    _, token_externo = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Externo",
        email="externo@email.com",
        equipe=equipe_b,
    )
    automacao = criar_automacao(client, token_criador, "Automação da equipe A")

    colega = client.get("/api/v1/automacoes", headers=headers(token_colega))
    externo = client.get("/api/v1/automacoes", headers=headers(token_externo))

    assert colega.status_code == 200
    assert [item["id"] for item in colega.json()["automacoes"]] == [
        automacao["id"]
    ]
    assert externo.status_code == 200
    assert externo.json()["automacoes"] == []


def test_equipe_inativa_bloqueia_criacao_e_listagem(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Inativa")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )
    with session_factory() as session:
        modelo = session.get(EquipeModel, UUID(equipe["id"]))
        assert modelo is not None
        modelo.ativa = False
        session.commit()

    criacao = client.post(
        "/api/v1/automacoes",
        json={"nome": "Automação bloqueada"},
        headers=headers(token),
    )
    listagem = client.get("/api/v1/automacoes", headers=headers(token))

    assert criacao.status_code == 409
    assert listagem.status_code == 409
    assert criacao.json()["detail"] == (
        "A equipe do usuário não está disponível."
    )


def test_listagem_vazia_e_paginacao_funcionam(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )
    vazia = client.get("/api/v1/automacoes", headers=headers(token))
    criar_automacao(client, token, "Automação um")
    criar_automacao(client, token, "Automação dois")
    criar_automacao(client, token, "Automação três")

    response = client.get(
        "/api/v1/automacoes?pagina=1&itens_por_pagina=2",
        headers=headers(token),
    )

    assert vazia.status_code == 200
    assert vazia.json()["automacoes"] == []
    assert response.status_code == 200
    dados = response.json()
    assert [item["nome"] for item in dados["automacoes"]] == [
        "Automação três",
        "Automação dois",
    ]
    assert dados["total"] == 3
    assert dados["total_paginas"] == 2


def test_dados_invalidos_retorna_422(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )

    nome_invalido = client.post(
        "/api/v1/automacoes",
        json={"nome": "  "},
        headers=headers(token),
    )
    descricao_invalida = client.post(
        "/api/v1/automacoes",
        json={"nome": "Automação", "descricao": "x" * 501},
        headers=headers(token),
    )

    assert nome_invalido.status_code == 422
    assert descricao_invalida.status_code == 422


def test_usuario_ativa_pausa_e_reativa_automacao_da_propria_equipe(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )
    automacao = criar_automacao(client, token, "Automação controlada")

    ativacao = client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        json={"status": "pausada"},
        headers=headers(token),
    )
    pausa = client.post(
        f"/api/v1/automacoes/{automacao['id']}/pausar",
        headers=headers(token),
    )
    reativacao = client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        headers=headers(token),
    )

    assert ativacao.status_code == 200
    assert ativacao.json()["status"] == "ativa"
    assert pausa.status_code == 200
    assert pausa.json()["status"] == "pausada"
    assert reativacao.status_code == 200
    assert reativacao.json()["status"] == "ativa"


def test_transicoes_invalidas_de_automacao_retornam_409(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )
    automacao = criar_automacao(client, token, "Automação controlada")

    pausa_em_rascunho = client.post(
        f"/api/v1/automacoes/{automacao['id']}/pausar",
        headers=headers(token),
    )
    client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        headers=headers(token),
    )
    ativacao_repetida = client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        headers=headers(token),
    )

    assert pausa_em_rascunho.status_code == 409
    assert pausa_em_rascunho.json()["detail"] == (
        "Não é possível alterar a automação de 'rascunho' para 'pausada'."
    )
    assert ativacao_repetida.status_code == 409
    assert ativacao_repetida.json()["detail"] == (
        "Não é possível alterar a automação de 'ativa' para 'ativa'."
    )


def test_usuario_nao_altera_automacao_de_outra_equipe(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe_a = criar_equipe(client, admin_token, "Equipe A")
    equipe_b = criar_equipe(client, admin_token, "Equipe B")
    _, token_a = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário A",
        email="usuario.a@email.com",
        equipe=equipe_a,
    )
    _, token_b = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário B",
        email="usuario.b@email.com",
        equipe=equipe_b,
    )
    automacao = criar_automacao(client, token_a, "Automação da equipe A")

    response = client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        headers=headers(token_b),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Automação não encontrada."
    with session_factory() as session:
        modelo = session.get(AutomacaoModel, UUID(automacao["id"]))
        assert modelo is not None
        assert modelo.status == "rascunho"


def test_usuario_sem_equipe_nao_altera_status_de_automacao(
    client: TestClient,
) -> None:
    cadastrar_usuario(client, "Usuário sem equipe", "sem.equipe@email.com")
    token = obter_token(client, "sem.equipe@email.com")

    response = client.post(
        f"/api/v1/automacoes/{uuid4()}/ativar",
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "O usuário precisa estar associado a uma equipe."
    )


def test_equipe_inativa_nao_altera_status_de_automacao(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Inativa")
    _, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )
    automacao = criar_automacao(client, token, "Automação bloqueada")
    with session_factory() as session:
        modelo = session.get(EquipeModel, UUID(equipe["id"]))
        assert modelo is not None
        modelo.ativa = False
        session.commit()

    response = client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A equipe do usuário não está disponível."
    )


def test_pausar_automacao_nao_altera_execucao_existente(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    usuario, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário",
        email="usuario@email.com",
        equipe=equipe,
    )
    automacao = criar_automacao(client, token, "Automação em execução")
    client.post(
        f"/api/v1/automacoes/{automacao['id']}/ativar",
        headers=headers(token),
    )
    execucao_id = uuid4()
    agora = datetime.now(timezone.utc)
    with session_factory() as session:
        session.add(
            ExecucaoModel(
                id=execucao_id,
                automacao_id=UUID(automacao["id"]),
                equipe_id=UUID(equipe["id"]),
                solicitada_por_usuario_id=UUID(usuario["id"]),
                status="processando",
                mensagem_erro=None,
                criada_em=agora,
                iniciada_em=agora,
                finalizada_em=None,
                atualizada_em=agora,
            )
        )
        session.commit()

    response = client.post(
        f"/api/v1/automacoes/{automacao['id']}/pausar",
        headers=headers(token),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "pausada"
    with session_factory() as session:
        execucao = session.get(ExecucaoModel, execucao_id)
        assert execucao is not None
        assert execucao.status == "processando"
