from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

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


def test_usuario_comum_nao_pode_listar_usuarios(client: TestClient) -> None:
    cadastrar_usuario(client, "Usuário comum", "comum@email.com")
    token = obter_token(client, "comum@email.com")

    response = client.get("/api/v1/usuarios", headers=headers(token))

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Você não possui permissão para executar esta ação."
    )


def test_administrador_lista_usuarios_com_paginacao(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    cadastrar_usuario(client, "Administrador", "admin@email.com")
    cadastrar_usuario(client, "Usuário um", "usuario1@email.com")
    cadastrar_usuario(client, "Usuário dois", "usuario2@email.com")
    tornar_administrador(session_factory, "admin@email.com")
    token = obter_token(client, "admin@email.com")

    response = client.get(
        "/api/v1/usuarios?pagina=1&itens_por_pagina=2",
        headers=headers(token),
    )

    assert response.status_code == 200
    dados = response.json()
    assert len(dados["usuarios"]) == 2
    assert dados["pagina"] == 1
    assert dados["itens_por_pagina"] == 2
    assert dados["total"] == 3
    assert dados["total_paginas"] == 2


def test_administrador_altera_perfil_de_outro_usuario(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    cadastrar_usuario(client, "Administrador", "admin@email.com")
    alvo = cadastrar_usuario(client, "Usuário alvo", "alvo@email.com")
    tornar_administrador(session_factory, "admin@email.com")
    token = obter_token(client, "admin@email.com")

    response = client.patch(
        f"/api/v1/usuarios/{alvo['id']}/perfil",
        json={"perfil_acesso": "administrador"},
        headers=headers(token),
    )

    assert response.status_code == 200
    assert response.json()["perfil_acesso"] == "administrador"


def test_administrador_nao_pode_rebaixar_a_si_mesmo(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    administrador = cadastrar_usuario(
        client,
        "Administrador",
        "admin@email.com",
    )
    tornar_administrador(session_factory, "admin@email.com")
    token = obter_token(client, "admin@email.com")

    response = client.patch(
        f"/api/v1/usuarios/{administrador['id']}/perfil",
        json={"perfil_acesso": "usuario"},
        headers=headers(token),
    )

    assert response.status_code == 409


def test_administrador_nao_pode_desativar_a_si_mesmo(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    administrador = cadastrar_usuario(
        client,
        "Administrador",
        "admin@email.com",
    )
    tornar_administrador(session_factory, "admin@email.com")
    token = obter_token(client, "admin@email.com")

    response = client.patch(
        f"/api/v1/usuarios/{administrador['id']}/status",
        json={"ativo": False},
        headers=headers(token),
    )

    assert response.status_code == 409


def test_alteracao_de_usuario_inexistente_retorna_404(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    cadastrar_usuario(client, "Administrador", "admin@email.com")
    tornar_administrador(session_factory, "admin@email.com")
    token = obter_token(client, "admin@email.com")

    response = client.patch(
        f"/api/v1/usuarios/{uuid4()}/status",
        json={"ativo": False},
        headers=headers(token),
    )

    assert response.status_code == 404


def test_usuario_desativado_perde_acesso_imediatamente(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    cadastrar_usuario(client, "Administrador", "admin@email.com")
    alvo = cadastrar_usuario(client, "Usuário alvo", "alvo@email.com")
    tornar_administrador(session_factory, "admin@email.com")
    admin_token = obter_token(client, "admin@email.com")
    alvo_token = obter_token(client, "alvo@email.com")

    alteracao = client.patch(
        f"/api/v1/usuarios/{alvo['id']}/status",
        json={"ativo": False},
        headers=headers(admin_token),
    )
    acesso = client.get(
        "/api/v1/autenticacao/usuario-atual",
        headers=headers(alvo_token),
    )

    assert alteracao.status_code == 200
    assert alteracao.json()["ativo"] is False
    assert acesso.status_code == 401
