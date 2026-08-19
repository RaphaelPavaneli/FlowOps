import type {
  CredenciaisLogin,
  TokenAutenticacao,
  UsuarioAutenticado,
} from "../types/autenticacao";

interface RespostaErroApi {
  detail?: string;
}

export class ErroAutenticacao extends Error {
  constructor(
    message: string,
    public readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ErroAutenticacao";
  }
}

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
      resposta.status,
    );
  }

  return resposta.json() as Promise<TokenAutenticacao>;
}

export async function obterUsuarioAtual(
  token: string,
): Promise<UsuarioAutenticado> {
  let resposta: Response;

  try {
    resposta = await fetch("/api/v1/autenticacao/usuario-atual", {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    throw new ErroAutenticacao(
      "Não foi possível validar sua sessão. Tente novamente em instantes.",
    );
  }

  if (!resposta.ok) {
    const erro = (await resposta.json().catch(() => ({}))) as RespostaErroApi;
    throw new ErroAutenticacao(
      erro.detail ?? "Sua sessão não é mais válida.",
      resposta.status,
    );
  }

  return resposta.json() as Promise<UsuarioAutenticado>;
}
