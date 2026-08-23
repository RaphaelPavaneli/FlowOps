import type { ResumoDashboardAdministrativo } from "../types/dashboard";

interface RespostaErroApi {
  detail?: string;
}

export class ErroDashboard extends Error {
  constructor(
    message: string,
    public readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ErroDashboard";
  }
}

export async function obterResumoDashboardAdministrativo(
  token: string,
): Promise<ResumoDashboardAdministrativo> {
  let resposta: Response;

  try {
    resposta = await fetch("/api/v1/dashboard/resumo-administrativo", {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    throw new ErroDashboard(
      "Não foi possível carregar o dashboard. Verifique sua conexão.",
    );
  }

  if (!resposta.ok) {
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroDashboard(
      erro.detail ?? "Não foi possível carregar o dashboard.",
      resposta.status,
    );
  }

  return resposta.json() as Promise<ResumoDashboardAdministrativo>;
}
