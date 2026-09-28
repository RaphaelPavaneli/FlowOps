import type {
  Execucao,
  ListaExecucoesResponse,
} from "../types/execucoes";

interface RespostaErroApi {
  detail?: string;
}

export class ErroExecucoes extends Error {
  constructor(
    message: string,
    public readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ErroExecucoes";
  }
}

export async function iniciarExecucao(
  token: string,
  automacaoId: string,
): Promise<Execucao> {
  let resposta: Response;

  try {
    resposta = await fetch(
      `/api/v1/automacoes/${automacaoId}/execucoes`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      },
    );
  } catch {
    throw new ErroExecucoes(
      "Não foi possível solicitar a execução. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    throw await criarErroExecucoes(
      resposta,
      "Não foi possível solicitar a execução.",
    );
  }

  return resposta.json() as Promise<Execucao>;
}

export async function listarExecucoes(
  token: string,
  automacaoId: string,
  pagina: number,
  itensPorPagina = 20,
): Promise<ListaExecucoesResponse> {
  const parametros = new URLSearchParams({
    pagina: String(pagina),
    itens_por_pagina: String(itensPorPagina),
  });

  let resposta: Response;

  try {
    resposta = await fetch(
      `/api/v1/automacoes/${automacaoId}/execucoes?${parametros}`,
      { headers: { Authorization: `Bearer ${token}` } },
    );
  } catch {
    throw new ErroExecucoes(
      "Não foi possível carregar o histórico. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    throw await criarErroExecucoes(
      resposta,
      "Não foi possível carregar o histórico de execuções.",
    );
  }

  return resposta.json() as Promise<ListaExecucoesResponse>;
}

async function criarErroExecucoes(
  resposta: Response,
  mensagemPadrao: string,
): Promise<ErroExecucoes> {
  const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
  return new ErroExecucoes(erro.detail ?? mensagemPadrao, resposta.status);
}
