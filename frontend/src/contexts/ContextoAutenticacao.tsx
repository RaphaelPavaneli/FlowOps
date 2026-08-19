import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  autenticar,
  obterUsuarioAtual,
} from "../services/autenticacao";
import type {
  CredenciaisLogin,
  UsuarioAutenticado,
} from "../types/autenticacao";

const CHAVE_TOKEN = "flowops:token";

interface ContextoAutenticacaoValor {
  token: string | null;
  usuario: UsuarioAutenticado | null;
  autenticado: boolean;
  carregandoSessao: boolean;
  entrar: (credenciais: CredenciaisLogin) => Promise<UsuarioAutenticado>;
  sair: () => void;
}

interface PropriedadesProvedor {
  children: ReactNode;
}

const ContextoAutenticacao = createContext<ContextoAutenticacaoValor | null>(
  null,
);

function lerTokenArmazenado(): string | null {
  return sessionStorage.getItem(CHAVE_TOKEN);
}

export function ProvedorAutenticacao({ children }: PropriedadesProvedor) {
  const [token, setToken] = useState<string | null>(lerTokenArmazenado);
  const [usuario, setUsuario] = useState<UsuarioAutenticado | null>(null);
  const [carregandoSessao, setCarregandoSessao] = useState(() =>
    Boolean(lerTokenArmazenado()),
  );

  function limparSessao() {
    sessionStorage.removeItem(CHAVE_TOKEN);
    setToken(null);
    setUsuario(null);
  }

  useEffect(() => {
    if (!token) {
      return;
    }

    let restauracaoAtiva = true;

    async function restaurarSessao() {
      try {
        const usuarioAtual = await obterUsuarioAtual(token as string);
        if (restauracaoAtiva) {
          setUsuario(usuarioAtual);
        }
      } catch {
        if (restauracaoAtiva) {
          limparSessao();
        }
      } finally {
        if (restauracaoAtiva) {
          setCarregandoSessao(false);
        }
      }
    }

    void restaurarSessao();

    return () => {
      restauracaoAtiva = false;
    };
  }, []);

  async function entrar(credenciais: CredenciaisLogin) {
    const resposta = await autenticar(credenciais);
    const usuarioAtual = await obterUsuarioAtual(resposta.access_token);

    sessionStorage.setItem(CHAVE_TOKEN, resposta.access_token);
    setToken(resposta.access_token);
    setUsuario(usuarioAtual);

    return usuarioAtual;
  }

  function sair() {
    limparSessao();
  }

  const valor = useMemo<ContextoAutenticacaoValor>(
    () => ({
      token,
      usuario,
      autenticado: usuario !== null,
      carregandoSessao,
      entrar,
      sair,
    }),
    [token, usuario, carregandoSessao],
  );

  return (
    <ContextoAutenticacao.Provider value={valor}>
      {children}
    </ContextoAutenticacao.Provider>
  );
}

export function useAutenticacao(): ContextoAutenticacaoValor {
  const contexto = useContext(ContextoAutenticacao);

  if (!contexto) {
    throw new Error(
      "useAutenticacao deve ser utilizado dentro de ProvedorAutenticacao.",
    );
  }

  return contexto;
}
