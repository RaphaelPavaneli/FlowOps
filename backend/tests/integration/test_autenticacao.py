from fastapi.testclient import TestClient


CADASTRO_VALIDO = {
    "nome": "Rafael",
    "email": "Rafael@Email.com",
    "senha": "uma senha longa e segura",
}


def test_cadastro_cria_usuario_com_perfil_seguro(client: TestClient) -> None:
    response = client.post(
        "/api/v1/autenticacao/cadastro",
        json=CADASTRO_VALIDO,
    )

    assert response.status_code == 201
    dados = response.json()
    assert dados["nome"] == "Rafael"
    assert dados["email"] == "rafael@email.com"
    assert dados["perfil_acesso"] == "usuario"
    assert dados["ativo"] is True
    assert "senha" not in dados
    assert "senha_hash" not in dados


def test_cadastro_rejeita_perfil_enviado_pelo_cliente(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/autenticacao/cadastro",
        json={**CADASTRO_VALIDO, "perfil_acesso": "administrador"},
    )

    assert response.status_code == 422


def test_cadastro_rejeita_email_duplicado(client: TestClient) -> None:
    client.post("/api/v1/autenticacao/cadastro", json=CADASTRO_VALIDO)

    response = client.post(
        "/api/v1/autenticacao/cadastro",
        json={**CADASTRO_VALIDO, "email": "rafael@email.com"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Já existe um usuário cadastrado com este e-mail."
    )


def test_login_e_usuario_atual(client: TestClient) -> None:
    client.post("/api/v1/autenticacao/cadastro", json=CADASTRO_VALIDO)

    login_response = client.post(
        "/api/v1/autenticacao/login",
        json={
            "email": "rafael@email.com",
            "senha": CADASTRO_VALIDO["senha"],
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert login_response.json()["token_type"] == "bearer"
    assert login_response.json()["expires_in"] == 900

    me_response = client.get(
        "/api/v1/autenticacao/usuario-atual",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "rafael@email.com"


def test_login_nao_revela_se_email_ou_senha_falhou(
    client: TestClient,
) -> None:
    client.post("/api/v1/autenticacao/cadastro", json=CADASTRO_VALIDO)
    mensagem_esperada = "E-mail ou senha inválidos."

    senha_errada = client.post(
        "/api/v1/autenticacao/login",
        json={"email": "rafael@email.com", "senha": "senha incorreta"},
    )
    email_inexistente = client.post(
        "/api/v1/autenticacao/login",
        json={"email": "ninguem@email.com", "senha": "senha incorreta"},
    )

    assert senha_errada.status_code == 401
    assert email_inexistente.status_code == 401
    assert senha_errada.json()["detail"] == mensagem_esperada
    assert email_inexistente.json()["detail"] == mensagem_esperada


def test_usuario_atual_rejeita_token_invalido(client: TestClient) -> None:
    response = client.get(
        "/api/v1/autenticacao/usuario-atual",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Token de acesso inválido ou expirado."
    )
