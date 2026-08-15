from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.autenticacao import (
    get_autenticar_usuario,
    get_cadastrar_usuario,
    get_usuario_atual,
)
from app.api.schemas.autenticacao import (
    CadastroRequest,
    LoginRequest,
    TokenResponse,
    UsuarioResponse,
)
from app.application.use_cases.autenticar_usuario import AutenticarUsuario
from app.application.use_cases.cadastrar_usuario import CadastrarUsuario
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.autenticacao import (
    CredenciaisInvalidasError,
    EmailJaCadastradoError,
)


router = APIRouter(prefix="/autenticacao", tags=["Autenticação"])


@router.post(
    "/cadastro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo usuário",
)
def cadastrar_usuario(
    dados: CadastroRequest,
    caso_de_uso: Annotated[CadastrarUsuario, Depends(get_cadastrar_usuario)],
) -> UsuarioResponse:
    try:
        usuario = caso_de_uso.executar(
            nome=dados.nome,
            email=str(dados.email),
            senha=dados.senha,
        )
    except EmailJaCadastradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com este e-mail.",
        ) from erro

    return UsuarioResponse.model_validate(usuario)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar com e-mail e senha",
)
def autenticar_usuario(
    dados: LoginRequest,
    caso_de_uso: Annotated[AutenticarUsuario, Depends(get_autenticar_usuario)],
) -> TokenResponse:
    try:
        resultado = caso_de_uso.executar(
            email=str(dados.email),
            senha=dados.senha,
        )
    except CredenciaisInvalidasError as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from erro

    return TokenResponse.model_validate(resultado, from_attributes=True)


@router.get(
    "/usuario-atual",
    response_model=UsuarioResponse,
    summary="Obter o usuário autenticado",
)
def obter_usuario_atual(
    usuario: Annotated[Usuario, Depends(get_usuario_atual)],
) -> UsuarioResponse:
    return UsuarioResponse.model_validate(usuario)
