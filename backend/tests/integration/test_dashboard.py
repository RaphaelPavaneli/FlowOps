from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.models.usuario_model import UsuarioModel
from app.infrastructure.database.repositories.sql_dashboard_repository import (
    SqlDashboardRepository,
)


SENHA_TESTE = "uma senha longa e segura"


def cadastrar_usuario(
    client: TestClient,
    nome: str,
    email: str,
) -> None:
    response = client.post(
        "/api/v1/autenticacao/cadastro",
        json={"nome": nome, "email": email, "senha": SENHA_TESTE},
    )
    assert response.status_code == 201


def alterar_usuario(
    session_factory: sessionmaker[Session],
    email: str,
    *,
    perfil_acesso: str | None = None,
    ativo: bool | None = None,
) -> None:
    with session_factory() as session:
        usuario = session.scalar(
            select(UsuarioModel).where(UsuarioModel.email == email)
        )
        assert usuario is not None
        if perfil_acesso is not None:
            usuario.perfil_acesso = perfil_acesso
        if ativo is not None:
            usuario.ativo = ativo
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


def test_dashboard_exige_autenticacao(client: TestClient) -> None:
    response = client.get("/api/v1/dashboard/resumo-administrativo")

    assert response.status_code == 401


def test_usuario_comum_nao_acessa_dashboard_administrativo(
    client: TestClient,
) -> None:
    cadastrar_usuario(client, "Usuário comum", "comum@email.com")
    token = obter_token(client, "comum@email.com")

    response = client.get(
        "/api/v1/dashboard/resumo-administrativo",
        headers=headers(token),
    )

    assert response.status_code == 403


def test_administrador_obtem_indicadores_de_usuarios(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    cadastrar_usuario(client, "Administrador", "admin@email.com")
    cadastrar_usuario(client, "Usuário ativo", "ativo@email.com")
    cadastrar_usuario(client, "Usuário inativo", "inativo@email.com")
    alterar_usuario(
        session_factory,
        "admin@email.com",
        perfil_acesso="administrador",
    )
    alterar_usuario(
        session_factory,
        "inativo@email.com",
        ativo=False,
    )
    token = obter_token(client, "admin@email.com")

    response = client.get(
        "/api/v1/dashboard/resumo-administrativo",
        headers=headers(token),
    )

    assert response.status_code == 200
    assert response.json() == {
        "usuarios": {
            "total": 3,
            "ativos": 2,
            "inativos": 1,
            "administradores": 1,
            "comuns": 2,
        }
    }


def test_repositorio_retorna_zeros_sem_usuarios(
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory() as session:
        resumo = SqlDashboardRepository(session).obter_resumo()

    assert resumo.usuarios.total == 0
    assert resumo.usuarios.ativos == 0
    assert resumo.usuarios.inativos == 0
    assert resumo.usuarios.administradores == 0
    assert resumo.usuarios.comuns == 0
