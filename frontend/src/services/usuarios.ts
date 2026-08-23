import type { PerfilAcesso } from "../types/autenticacao";
import type {
  AlterarPerfilUsuarioRequest,
  AlterarStatusUsuarioRequest,
  ListaUsuariosResponse,
  UsuarioAdministracao,
} from "../types/usuarios";

interface RespostaErroApi {
  detail?: string;
}

export class ErroUsuarios extends Error {
  constructor(
    message: string,
    public readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ErroUsuarios";
  }
}

export async function listarUsuarios(
  token: string,
  pagina: number,
  itensPorPagina = 20,
): Promise<ListaUsuariosResponse> {
  const parametros = new URLSearchParams({
    pagina: String(pagina),
    itens_por_pagina: String(itensPorPagina),
  });

  let resposta: Response;

  try {
    resposta = await fetch(`/api/v1/usuarios?${parametros}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    throw new ErroUsuarios(
      "Não foi possível carregar os usuários. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroUsuarios(
      erro.detail ?? "Não foi possível carregar os usuários.",
      resposta.status,
    );
  }

  return resposta.json() as Promise<ListaUsuariosResponse>;
}

export async function alterarPerfilUsuario(
  token: string,
  usuarioId: string,
  perfilAcesso: PerfilAcesso,
): Promise<UsuarioAdministracao> {
  const dados: AlterarPerfilUsuarioRequest = {
    perfil_acesso: perfilAcesso,
  };

  return alterarUsuario(
    token,
    `/api/v1/usuarios/${usuarioId}/perfil`,
    dados,
    "Não foi possível alterar o perfil do usuário.",
  );
}

export async function alterarStatusUsuario(
  token: string,
  usuarioId: string,
  ativo: boolean,
): Promise<UsuarioAdministracao> {
  const dados: AlterarStatusUsuarioRequest = { ativo };

  return alterarUsuario(
    token,
    `/api/v1/usuarios/${usuarioId}/status`,
    dados,
    `Não foi possível ${ativo ? "ativar" : "desativar"} o usuário.`,
  );
}

async function alterarUsuario(
  token: string,
  url: string,
  dados: AlterarPerfilUsuarioRequest | AlterarStatusUsuarioRequest,
  mensagemPadrao: string,
): Promise<UsuarioAdministracao> {
  let resposta: Response;

  try {
    resposta = await fetch(url, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });
  } catch {
    throw new ErroUsuarios(
      "Não foi possível concluir a alteração. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroUsuarios(
      erro.detail ?? mensagemPadrao,
      resposta.status,
    );
  }

  return resposta.json() as Promise<UsuarioAdministracao>;
}
