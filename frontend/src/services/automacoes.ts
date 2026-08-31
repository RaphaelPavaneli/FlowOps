import type {
  Automacao,
  CriarAutomacaoRequest,
  ListaAutomacoesResponse,
} from "../types/automacoes";

interface RespostaErroApi {
  detail?: string;
}

export class ErroAutomacoes extends Error {
  constructor(
    message: string,
    public readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ErroAutomacoes";
  }
}

export async function listarAutomacoes(
  token: string,
  pagina: number,
  itensPorPagina = 20,
): Promise<ListaAutomacoesResponse> {
  const parametros = new URLSearchParams({
    pagina: String(pagina),
    itens_por_pagina: String(itensPorPagina),
  });

  let resposta: Response;

  try {
    resposta = await fetch(`/api/v1/automacoes?${parametros}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    throw new ErroAutomacoes(
      "Não foi possível carregar as automações. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    throw await criarErroAutomacoes(
      resposta,
      "Não foi possível carregar as automações.",
    );
  }

  return resposta.json() as Promise<ListaAutomacoesResponse>;
}

export async function criarAutomacao(
  token: string,
  dados: CriarAutomacaoRequest,
): Promise<Automacao> {
  let resposta: Response;

  try {
    resposta = await fetch("/api/v1/automacoes", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });
  } catch {
    throw new ErroAutomacoes(
      "Não foi possível criar a automação. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    throw await criarErroAutomacoes(
      resposta,
      "Não foi possível criar a automação.",
    );
  }

  return resposta.json() as Promise<Automacao>;
}

async function criarErroAutomacoes(
  resposta: Response,
  mensagemPadrao: string,
): Promise<ErroAutomacoes> {
  const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
  return new ErroAutomacoes(erro.detail ?? mensagemPadrao, resposta.status);
}
