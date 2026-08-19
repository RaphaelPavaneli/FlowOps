import { LogOut, ShieldCheck } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import { Marca } from "./Marca";

function obterIniciais(nome: string) {
  return nome
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((parte) => parte[0])
    .join("")
    .toUpperCase();
}

export function LayoutAutenticado() {
  const { usuario, sair } = useAutenticacao();

  if (!usuario) {
    return null;
  }

  const administrador = usuario.perfil_acesso === "administrador";

  return (
    <div className="layout-autenticado">
      <header className="cabecalho-app">
        <div className="container conteudo-cabecalho-app">
          <Marca />

          <nav className="navegacao-app" aria-label="Navegação da aplicação">
            <NavLink to="/app" end>
              Minha conta
            </NavLink>
            {administrador && (
              <>
                <NavLink to="/app/dashboard">Dashboard</NavLink>
                <NavLink to="/app/administracao">Administração</NavLink>
              </>
            )}
          </nav>

          <div className="conta-cabecalho-app">
            <span className="avatar-usuario" aria-hidden="true">
              {obterIniciais(usuario.nome)}
            </span>
            <span className="identificacao-usuario">
              <strong>{usuario.nome}</strong>
              <small>
                {administrador && <ShieldCheck size={12} aria-hidden="true" />}
                {administrador ? "Administrador" : "Usuário"}
              </small>
            </span>
            <button className="botao-sair" type="button" onClick={sair}>
              <LogOut size={17} aria-hidden="true" />
              <span>Sair</span>
            </button>
          </div>
        </div>
      </header>

      <Outlet />
    </div>
  );
}
