from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.models.equipe_model import EquipeModel
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


def criar_equipe(client: TestClient, token: str, nome: str) -> dict:
    response = client.post(
        "/api/v1/equipes",
        json={"nome": nome},
        headers=headers(token),
    )
    assert response.status_code == 201
    return response.json()


def test_equipe_exige_autenticacao(client: TestClient) -> None:
    response = client.get("/api/v1/equipes")

    assert response.status_code == 401


def test_usuario_comum_nao_pode_gerenciar_equipes(client: TestClient) -> None:
    usuario = cadastrar_usuario(client, "Usuário comum", "comum@email.com")
    token = obter_token(client, "comum@email.com")

    criacao = client.post(
        "/api/v1/equipes",
        json={"nome": "Equipe Financeiro"},
        headers=headers(token),
    )
    listagem = client.get("/api/v1/equipes", headers=headers(token))
    associacao = client.put(
        f"/api/v1/equipes/{uuid4()}/membros/{usuario['id']}",
        headers=headers(token),
    )

    assert usuario["equipe_id"] is None
    assert criacao.status_code == 403
    assert listagem.status_code == 403
    assert associacao.status_code == 403


def test_administrador_cria_equipe_ativa_com_nome_limpo(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)

    response = client.post(
        "/api/v1/equipes",
        json={"nome": "  Equipe Financeiro  "},
        headers=headers(token),
    )

    assert response.status_code == 201
    assert response.json()["nome"] == "Equipe Financeiro"
    assert response.json()["ativa"] is True


def test_nome_invalido_da_equipe_retorna_422(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)

    response = client.post(
        "/api/v1/equipes",
        json={"nome": "  "},
        headers=headers(token),
    )

    assert response.status_code == 422


def test_administrador_lista_equipes_com_paginacao(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)
    criar_equipe(client, token, "Equipe C")
    criar_equipe(client, token, "Equipe A")
    criar_equipe(client, token, "Equipe B")

    response = client.get(
        "/api/v1/equipes?pagina=1&itens_por_pagina=2",
        headers=headers(token),
    )

    assert response.status_code == 200
    dados = response.json()
    assert [equipe["nome"] for equipe in dados["equipes"]] == [
        "Equipe A",
        "Equipe B",
    ]
    assert dados["total"] == 3
    assert dados["total_paginas"] == 2


def test_administrador_associa_usuario_a_equipe(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)
    usuario = cadastrar_usuario(client, "Usuário alvo", "alvo@email.com")
    equipe = criar_equipe(client, token, "Equipe Operações")

    response = client.put(
        f"/api/v1/equipes/{equipe['id']}/membros/{usuario['id']}",
        headers=headers(token),
    )

    assert response.status_code == 200
    assert response.json()["equipe_id"] == equipe["id"]


def test_usuario_atual_reflete_troca_de_equipe_sem_novo_login(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    admin_token = preparar_administrador(client, session_factory)
    usuario = cadastrar_usuario(client, "Usuário alvo", "alvo@email.com")
    usuario_token = obter_token(client, "alvo@email.com")
    primeira = criar_equipe(client, admin_token, "Equipe Um")
    segunda = criar_equipe(client, admin_token, "Equipe Dois")
    client.put(
        f"/api/v1/equipes/{primeira['id']}/membros/{usuario['id']}",
        headers=headers(admin_token),
    )

    alteracao = client.put(
        f"/api/v1/equipes/{segunda['id']}/membros/{usuario['id']}",
        headers=headers(admin_token),
    )
    usuario_atual = client.get(
        "/api/v1/autenticacao/usuario-atual",
        headers=headers(usuario_token),
    )

    assert alteracao.status_code == 200
    assert usuario_atual.status_code == 200
    assert usuario_atual.json()["equipe_id"] == segunda["id"]


def test_associacao_com_equipe_inexistente_retorna_404(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)
    usuario = cadastrar_usuario(client, "Usuário alvo", "alvo@email.com")

    response = client.put(
        f"/api/v1/equipes/{uuid4()}/membros/{usuario['id']}",
        headers=headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Equipe não encontrada."


def test_associacao_com_usuario_inexistente_retorna_404(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, token, "Equipe Operações")

    response = client.put(
        f"/api/v1/equipes/{equipe['id']}/membros/{uuid4()}",
        headers=headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."


def test_equipe_inativa_nao_aceita_novo_membro(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    token = preparar_administrador(client, session_factory)
    usuario = cadastrar_usuario(client, "Usuário alvo", "alvo@email.com")
    equipe = criar_equipe(client, token, "Equipe Inativa")
    with session_factory() as session:
        modelo = session.get(EquipeModel, UUID(equipe["id"]))
        assert modelo is not None
        modelo.ativa = False
        session.commit()

    response = client.put(
        f"/api/v1/equipes/{equipe['id']}/membros/{usuario['id']}",
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Não é possível associar usuários a uma equipe inativa."
    )
