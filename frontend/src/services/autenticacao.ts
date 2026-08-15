import type {
  CredenciaisLogin,
  TokenAutenticacao,
} from "../types/autenticacao";

interface RespostaErroApi {
  detail?: string;
}

export class ErroAutenticacao extends Error {}

export async function autenticar(
  credenciais: CredenciaisLogin,
): Promise<TokenAutenticacao> {
  let resposta: Response;

  try {
    resposta = await fetch("/api/v1/autenticacao/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credenciais),
    });
  } catch {
    throw new ErroAutenticacao(
      "Não foi possível conectar ao servidor. Tente novamente em instantes.",
    );
  }

  if (!resposta.ok) {
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroAutenticacao(
      erro.detail ?? "Não foi possível entrar. Verifique os dados informados.",
    );
  }

  return resposta.json() as Promise<TokenAutenticacao>;
}
