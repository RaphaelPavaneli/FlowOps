import { useEffect } from "react";
import {
  BadgeCheck,
  Mail,
  ShieldCheck,
  UserRound,
} from "lucide-react";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";

function formatarPerfil(perfil: "administrador" | "usuario") {
  return perfil === "administrador" ? "Administrador" : "Usuário";
}

export function PaginaAreaAutenticada() {
  const { usuario } = useAutenticacao();

  useEffect(() => {
    document.title = "Área autenticada | FlowOps";
  }, []);

  if (!usuario) {
    return null;
  }

  return (
    <main className="pagina-area-autenticada">
      <div className="container conteudo-area-autenticada">
        <section className="boas-vindas-area" aria-labelledby="titulo-area">
          <span className="etiqueta-home">
            <ShieldCheck size={15} aria-hidden="true" />
            Sessão protegida
          </span>
          <h1 id="titulo-area">Bem-vindo, {usuario.nome}</h1>
          <p>
            Sua identidade foi validada pelo backend e sua sessão está ativa
            nesta aba.
          </p>
        </section>

        <section className="cartao-sessao" aria-labelledby="titulo-sessao">
          <div className="cabecalho-cartao-sessao">
            <div className="icone-usuario-sessao" aria-hidden="true">
              <UserRound size={24} />
            </div>
            <div>
              <span>Usuário autenticado</span>
              <h2 id="titulo-sessao">Informações da sua conta</h2>
            </div>
            <span className="status-sessao">
              <span aria-hidden="true" /> Ativa
            </span>
          </div>

          <dl className="dados-sessao">
            <div>
              <dt><Mail size={17} aria-hidden="true" /> E-mail</dt>
              <dd>{usuario.email}</dd>
            </div>
            <div>
              <dt><BadgeCheck size={17} aria-hidden="true" /> Perfil</dt>
              <dd>{formatarPerfil(usuario.perfil_acesso)}</dd>
            </div>
          </dl>
        </section>
      </div>
    </main>
  );
}
