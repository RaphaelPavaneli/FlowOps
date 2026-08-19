import { useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

import { Marca } from "../components/Marca";

export function PaginaNaoEncontrada() {
  useEffect(() => {
    document.title = "Página não encontrada | FlowOps";
  }, []);

  return (
    <main className="pagina-nao-encontrada">
      <Marca />
      <div>
        <span>Erro 404</span>
        <h1>Esta página não foi encontrada.</h1>
        <p>O endereço pode estar incorreto ou a página pode ter sido movida.</p>
        <Link className="botao botao-primario" to="/">
          <ArrowLeft size={18} aria-hidden="true" />
          Voltar para o início
        </Link>
      </div>
    </main>
  );
}
