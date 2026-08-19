import { useEffect } from "react";
import {
  ArrowLeft,
  BadgeCheck,
  LockKeyhole,
  Settings2,
  UsersRound,
} from "lucide-react";
import { Link } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";

export function PaginaAdministracao() {
  const { usuario } = useAutenticacao();

  useEffect(() => {
    document.title = "Administração | FlowOps";
  }, []);

  return (
    <main className="pagina-administracao">
      <div className="container conteudo-administracao">
        <Link className="link-voltar-dashboard" to="/app/dashboard">
          <ArrowLeft size={17} aria-hidden="true" />
          Voltar ao dashboard
        </Link>

        <section className="cabecalho-administracao">
          <span className="icone-pagina-administracao" aria-hidden="true">
            <Settings2 size={25} />
          </span>
          <div>
            <span className="sobretitulo">Área exclusiva</span>
            <h1>Administração</h1>
            <p>Gerencie os recursos administrativos disponíveis no FlowOps.</p>
          </div>
        </section>

        <section className="grade-modulos-administracao">
          <article className="cartao-modulo-administracao">
            <span className="icone-modulo-administracao"><UsersRound size={23} /></span>
            <div>
              <span>Próxima etapa</span>
              <h2>Gerenciamento de usuários</h2>
              <p>Gerencie perfis, permissões e o estado das contas da plataforma.</p>
            </div>
            <span className="selo-proxima-etapa">Em breve</span>
          </article>

          <article className="cartao-identidade-administrador">
            <div className="titulo-identidade-administrador">
              <span className="icone-modulo-administracao"><LockKeyhole size={21} /></span>
              <div>
                <span>Sessão atual</span>
                <h2>Administrador autenticado</h2>
              </div>
            </div>
            <dl>
              <div>
                <dt>Nome</dt>
                <dd>{usuario?.nome}</dd>
              </div>
              <div>
                <dt>E-mail</dt>
                <dd>{usuario?.email}</dd>
              </div>
              <div>
                <dt>Perfil</dt>
                <dd><BadgeCheck size={15} /> Administrador</dd>
              </div>
            </dl>
          </article>
        </section>
      </div>
    </main>
  );
}
