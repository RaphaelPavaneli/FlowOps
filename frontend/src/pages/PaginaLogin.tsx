import { useEffect } from "react";

import { FormularioLogin } from "../components/FormularioLogin";
import { Marca } from "../components/Marca";

export function PaginaLogin() {
  useEffect(() => {
    document.title = "Entrar | FlowOps";
  }, []);

  return (
    <main className="pagina-login">
      <div className="brilho brilho-superior" aria-hidden="true" />
      <div className="brilho brilho-inferior" aria-hidden="true" />
      <div className="forma-abstrata forma-superior" aria-hidden="true" />
      <div className="forma-abstrata forma-inferior" aria-hidden="true" />

      <header className="cabecalho-login">
        <Marca />
      </header>

      <section className="conteudo-login" aria-labelledby="titulo-login">
        <FormularioLogin />
      </section>

      <footer className="rodape-login">
        © {new Date().getFullYear()} FlowOps. Gestão que flui com você.
      </footer>
    </main>
  );
}
