import { useEffect } from "react";
import { ArrowLeft, ShieldX } from "lucide-react";
import { Link } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";

export function PaginaAcessoNegado() {
  const { usuario } = useAutenticacao();
  const destino = usuario?.perfil_acesso === "administrador" ? "/app/dashboard" : "/app";

  useEffect(() => {
    document.title = "Acesso negado | FlowOps";
  }, []);

  return (
    <main className="pagina-acesso-negado">
      <span className="icone-acesso-negado"><ShieldX size={30} /></span>
      <span className="sobretitulo">Acesso restrito</span>
      <h1>Você não possui permissão para acessar esta página.</h1>
      <p>Seu perfil continua autenticado, mas esta área exige outra permissão.</p>
      <Link className="botao botao-primario" to={destino}>
        <ArrowLeft size={18} aria-hidden="true" />
        Voltar para minha área
      </Link>
    </main>
  );
}
