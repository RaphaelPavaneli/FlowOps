import type { UsuarioAdministracao } from "../types/usuarios";
import type {
  CriarEquipeRequest,
  Equipe,
  ListaEquipesResponse,
} from "../types/equipes";

interface RespostaErroApi {
  detail?: string;
}

export class ErroEquipes extends Error {
  constructor(
    message: string,
    public readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ErroEquipes";
  }
}

export async function listarEquipes(
  token: string,
  pagina = 1,
  itensPorPagina = 100,
): Promise<ListaEquipesResponse> {
  const parametros = new URLSearchParams({
    pagina: String(pagina),
    itens_por_pagina: String(itensPorPagina),
  });

  return executarRequisicao<ListaEquipesResponse>(
    `/api/v1/equipes?${parametros}`,
    token,
    {},
    "Não foi possível carregar as equipes.",
  );
}

export async function criarEquipe(
  token: string,
  dados: CriarEquipeRequest,
): Promise<Equipe> {
  return executarRequisicao<Equipe>(
    "/api/v1/equipes",
    token,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    },
    "Não foi possível criar a equipe.",
  );
}

export async function associarUsuarioEquipe(
  token: string,
  equipeId: string,
  usuarioId: string,
): Promise<UsuarioAdministracao> {
  return executarRequisicao<UsuarioAdministracao>(
    `/api/v1/equipes/${equipeId}/membros/${usuarioId}`,
    token,
    { method: "PUT" },
    "Não foi possível associar o usuário à equipe.",
  );
}

async function executarRequisicao<T>(
  url: string,
  token: string,
  opcoes: RequestInit,
  mensagemPadrao: string,
): Promise<T> {
  let resposta: Response;

  try {
    resposta = await fetch(url, {
      ...opcoes,
      headers: {
        Authorization: `Bearer ${token}`,
        ...opcoes.headers,
      },
    });
  } catch {
    throw new ErroEquipes(
      `${mensagemPadrao} Verifique sua conexão.`,
    );
  }

  if (!resposta.ok) {
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroEquipes(
      erro.detail ?? mensagemPadrao,
      resposta.status,
    );
  }

  return resposta.json() as Promise<T>;
}
