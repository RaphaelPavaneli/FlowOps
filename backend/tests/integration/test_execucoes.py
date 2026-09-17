from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.models.equipe_model import EquipeModel
from app.infrastructure.database.models.usuario_model import UsuarioModel
from app.infrastructure.database.repositories.sql_execucao_repository import (
    SqlExecucaoRepository,
)


SENHA_TESTE = "uma senha longa e segura"


def cadastrar_usuario(client: TestClient, nome: str, email: str) -> dict:
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


def preparar_usuario_com_equipe(
    client: TestClient,
    admin_token: str,
    *,
    nome: str,
    email: str,
    equipe: dict,
) -> tuple[dict, str]:
    usuario = cadastrar_usuario(client, nome, email)
    associacao = client.put(
        f"/api/v1/equipes/{equipe['id']}/membros/{usuario['id']}",
        headers=headers(admin_token),
    )
    assert associacao.status_code == 200
    return usuario, obter_token(client, email)


def criar_automacao(client: TestClient, token: str, nome: str) -> dict:
    response = client.post(
        "/api/v1/automacoes",
        json={"nome": nome},
        headers=headers(token),
    )
    assert response.status_code == 201
    return response.json()


def ativar_automacao(
    client: TestClient,
    token: str,
    automacao_id: str,
) -> None:
    response = client.post(
        f"/api/v1/automacoes/{automacao_id}/ativar",
        headers=headers(token),
    )
    assert response.status_code == 200


def preparar_automacao_ativa(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> tuple[dict, dict, dict, str]:
    admin_token = preparar_administrador(client, session_factory)
    equipe = criar_equipe(client, admin_token, "Equipe Operações")
    usuario, token = preparar_usuario_com_equipe(
        client,
        admin_token,
        nome="Usuário executor",
        email="executor@email.com",
        equipe=equipe,
    )
    automacao = criar_automacao(client, token, "Automação executável")
    ativar_automacao(client, token, automacao["id"])
    return equipe, usuario, automacao, token


def test_inicio_de_execucao_exige_autenticacao(client: TestClient) -> None:
    response = client.post(
        f"/api/v1/automacoes/{uuid4()}/execucoes",
    )

    assert response.status_code == 401


def test_usuario_inicia_execucao_pendente_da_automacao_ativa(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    equipe, usuario, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )

    response = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token),
    )

    assert response.status_code == 201
    dados = response.json()
    assert dados["automacao_id"] == automacao["id"]
    assert dados["equipe_id"] == equipe["id"]
    assert dados["solicitada_por_usuario_id"] == usuario["id"]
    assert dados["status"] == "pendente"
    assert dados["mensagem_erro"] is None
    assert dados["iniciada_em"] is None
    assert dados["finalizada_em"] is None

    with session_factory() as session:
        repositorio = SqlExecucaoRepository(session)
        execucao = repositorio.buscar_por_id_e_equipe(
            UUID(dados["id"]),
            UUID(equipe["id"]),
        )

    assert execucao is not None
    assert execucao.status.value == "pendente"


@pytest.mark.parametrize("status", ["rascunho", "pausada"])
def test_automacao_indisponivel_nao_inicia_execucao(
    client: TestClient,
    session_factory: sessionmaker[Session],
    status: str,
) -> None:
    _, _, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )
    if status == "rascunho":
        outra_automacao = criar_automacao(client, token, "Automação rascunho")
        automacao_id = outra_automacao["id"]
    else:
        pausa = client.post(
            f"/api/v1/automacoes/{automacao['id']}/pausar",
            headers=headers(token),
        )
        assert pausa.status_code == 200
        automacao_id = automacao["id"]

    response = client.post(
        f"/api/v1/automacoes/{automacao_id}/execucoes",
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A automação precisa estar ativa para ser executada."
    )


def test_automacao_inexistente_ou_de_outra_equipe_retorna_404(
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
    ativar_automacao(client, token_a, automacao["id"])

    outra_equipe = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token_b),
    )
    inexistente = client.post(
        f"/api/v1/automacoes/{uuid4()}/execucoes",
        headers=headers(token_b),
    )

    assert outra_equipe.status_code == 404
    assert inexistente.status_code == 404
    assert outra_equipe.json()["detail"] == "Automação não encontrada."
    assert inexistente.json()["detail"] == "Automação não encontrada."


def test_usuario_sem_equipe_nao_inicia_execucao(client: TestClient) -> None:
    cadastrar_usuario(client, "Usuário sem equipe", "sem.equipe@email.com")
    token = obter_token(client, "sem.equipe@email.com")

    response = client.post(
        f"/api/v1/automacoes/{uuid4()}/execucoes",
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "O usuário precisa estar associado a uma equipe."
    )


def test_equipe_inativa_nao_inicia_execucao(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    equipe, _, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )
    with session_factory() as session:
        modelo = session.get(EquipeModel, UUID(equipe["id"]))
        assert modelo is not None
        modelo.ativa = False
        session.commit()

    response = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A equipe do usuário não está disponível."
    )


@pytest.mark.parametrize(
    "campo",
    ["status", "equipe_id", "solicitada_por_usuario_id"],
)
def test_cliente_nao_define_campos_protegidos_da_execucao(
    client: TestClient,
    session_factory: sessionmaker[Session],
    campo: str,
) -> None:
    _, _, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )

    response = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        json={campo: str(uuid4())},
        headers=headers(token),
    )

    assert response.status_code == 422


def test_endpoint_de_execucoes_esta_documentado_no_openapi(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    operacao = response.json()["paths"][
        "/api/v1/automacoes/{automacao_id}/execucoes"
    ]["post"]
    assert "Execuções" in operacao["tags"]
    assert "201" in operacao["responses"]


def test_consultas_de_execucao_exigem_autenticacao(
    client: TestClient,
) -> None:
    historico = client.get(
        f"/api/v1/automacoes/{uuid4()}/execucoes",
    )
    detalhes = client.get(f"/api/v1/execucoes/{uuid4()}")

    assert historico.status_code == 401
    assert detalhes.status_code == 401


def test_historico_de_execucoes_e_paginado_e_ordenado(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    _, _, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )
    vazio = client.get(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token),
    )
    execucoes = [
        client.post(
            f"/api/v1/automacoes/{automacao['id']}/execucoes",
            headers=headers(token),
        ).json()
        for _ in range(3)
    ]

    response = client.get(
        f"/api/v1/automacoes/{automacao['id']}/execucoes"
        "?pagina=1&itens_por_pagina=2",
        headers=headers(token),
    )

    assert vazio.status_code == 200
    assert vazio.json()["execucoes"] == []
    assert vazio.json()["total_paginas"] == 0
    assert response.status_code == 200
    dados = response.json()
    assert [item["id"] for item in dados["execucoes"]] == [
        execucoes[2]["id"],
        execucoes[1]["id"],
    ]
    assert dados["pagina"] == 1
    assert dados["itens_por_pagina"] == 2
    assert dados["total"] == 3
    assert dados["total_paginas"] == 2


def test_usuario_consulta_detalhes_da_execucao_da_propria_equipe(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    equipe, usuario, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )
    criacao = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token),
    )
    execucao = criacao.json()

    response = client.get(
        f"/api/v1/execucoes/{execucao['id']}",
        headers=headers(token),
    )

    assert response.status_code == 200
    dados = response.json()
    assert dados["id"] == execucao["id"]
    assert dados["automacao_id"] == automacao["id"]
    assert dados["equipe_id"] == equipe["id"]
    assert dados["solicitada_por_usuario_id"] == usuario["id"]
    assert dados["status"] == "pendente"
    assert dados["mensagem_erro"] is None
    assert dados["iniciada_em"] is None
    assert dados["finalizada_em"] is None


def test_historico_e_detalhes_nao_vazam_entre_equipes(
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
    ativar_automacao(client, token_a, automacao["id"])
    execucao = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token_a),
    ).json()

    historico_externo = client.get(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token_b),
    )
    historico_inexistente = client.get(
        f"/api/v1/automacoes/{uuid4()}/execucoes",
        headers=headers(token_b),
    )
    detalhe_externo = client.get(
        f"/api/v1/execucoes/{execucao['id']}",
        headers=headers(token_b),
    )
    detalhe_inexistente = client.get(
        f"/api/v1/execucoes/{uuid4()}",
        headers=headers(token_b),
    )

    assert historico_externo.status_code == 404
    assert historico_inexistente.status_code == 404
    assert historico_externo.json() == historico_inexistente.json()
    assert detalhe_externo.status_code == 404
    assert detalhe_inexistente.status_code == 404
    assert detalhe_externo.json() == detalhe_inexistente.json()


def test_usuario_sem_equipe_nao_consulta_execucoes(
    client: TestClient,
) -> None:
    cadastrar_usuario(client, "Usuário sem equipe", "sem.equipe@email.com")
    token = obter_token(client, "sem.equipe@email.com")

    historico = client.get(
        f"/api/v1/automacoes/{uuid4()}/execucoes",
        headers=headers(token),
    )
    detalhes = client.get(
        f"/api/v1/execucoes/{uuid4()}",
        headers=headers(token),
    )

    assert historico.status_code == 409
    assert detalhes.status_code == 409
    assert historico.json()["detail"] == (
        "O usuário precisa estar associado a uma equipe."
    )
    assert detalhes.json() == historico.json()


def test_equipe_inativa_nao_consulta_execucoes(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    equipe, _, automacao, token = preparar_automacao_ativa(
        client,
        session_factory,
    )
    execucao = client.post(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token),
    ).json()
    with session_factory() as session:
        modelo = session.get(EquipeModel, UUID(equipe["id"]))
        assert modelo is not None
        modelo.ativa = False
        session.commit()

    historico = client.get(
        f"/api/v1/automacoes/{automacao['id']}/execucoes",
        headers=headers(token),
    )
    detalhes = client.get(
        f"/api/v1/execucoes/{execucao['id']}",
        headers=headers(token),
    )

    assert historico.status_code == 409
    assert detalhes.status_code == 409
    assert historico.json()["detail"] == (
        "A equipe do usuário não está disponível."
    )
    assert detalhes.json() == historico.json()


def test_consultas_de_execucao_estao_documentadas_no_openapi(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    caminhos = response.json()["paths"]
    historico = caminhos[
        "/api/v1/automacoes/{automacao_id}/execucoes"
    ]["get"]
    detalhes = caminhos["/api/v1/execucoes/{execucao_id}"]["get"]
    assert "Execuções" in historico["tags"]
    assert "Execuções" in detalhes["tags"]
    assert "200" in historico["responses"]
    assert "200" in detalhes["responses"]
