import type { Execucao } from "../types/execucoes";

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
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroExecucoes(
      erro.detail ?? "Não foi possível solicitar a execução.",
      resposta.status,
    );
  }

  return resposta.json() as Promise<Execucao>;
}
