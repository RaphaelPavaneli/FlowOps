"""Casos de uso da aplicação."""

from app.application.use_cases.autenticar_usuario import (
    AutenticarUsuario,
    ResultadoAutenticacao,
)
from app.application.use_cases.alterar_perfil_usuario import AlterarPerfilUsuario
from app.application.use_cases.alterar_status_usuario import AlterarStatusUsuario
from app.application.use_cases.cadastrar_usuario import CadastrarUsuario
from app.application.use_cases.listar_usuarios import (
    ListarUsuarios,
    ResultadoListaUsuarios,
)
from app.application.use_cases.obter_usuario_atual import ObterUsuarioAtual

__all__ = [
    "AutenticarUsuario",
    "AlterarPerfilUsuario",
    "AlterarStatusUsuario",
    "CadastrarUsuario",
    "ListarUsuarios",
    "ObterUsuarioAtual",
    "ResultadoAutenticacao",
    "ResultadoListaUsuarios",
]
