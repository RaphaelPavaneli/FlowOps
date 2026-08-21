import type { ListaUsuariosResponse } from "../types/usuarios";

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
