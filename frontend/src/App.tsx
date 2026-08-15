import { FormularioLogin } from "./components/FormularioLogin";

function App() {
  return (
    <main className="pagina-login">
      <div className="brilho brilho-superior" aria-hidden="true" />
      <div className="brilho brilho-inferior" aria-hidden="true" />
      <div className="forma-abstrata forma-superior" aria-hidden="true" />
      <div className="forma-abstrata forma-inferior" aria-hidden="true" />

      <header className="cabecalho-login">
        <a className="marca" href="/" aria-label="FlowOps — início">
          <span className="simbolo-marca" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>
          <span>FlowOps</span>
        </a>
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

export default App;
