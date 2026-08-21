import { useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

import { Marca } from "../components/Marca";

export function PaginaNaoEncontrada() {
  useEffect(() => {
    document.title = "Página não encontrada | FlowOps";
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-[radial-gradient(circle_at_50%_20%,rgba(191,219,254,0.45),transparent_32%),#f9fbff] p-6 text-center sm:p-8">
      <Marca />
      <div className="mt-[58px] max-w-[520px]">
        <span className="text-xs font-bold tracking-[0.1em] text-flowops-700 uppercase">
          Erro 404
        </span>
        <h1 className="my-3.5 text-[clamp(2rem,5vw,3rem)] leading-tight font-bold tracking-[-0.10625rem] text-flowops-texto">
          Esta página não foi encontrada.
        </h1>
        <p className="mb-7 leading-[1.7] text-flowops-cinza">
          O endereço pode estar incorreto ou a página pode ter sido movida.
        </p>
        <Link
          className="inline-flex min-h-11.5 items-center justify-center gap-2.5 rounded-xl bg-linear-to-r from-flowops-700 to-flowops-500 px-5 text-[13.5px] font-bold text-white no-underline shadow-[0_12px_24px_rgba(37,99,235,0.2)] transition-[transform,box-shadow] duration-150 hover:-translate-y-px hover:shadow-[0_15px_30px_rgba(37,99,235,0.27)]"
          to="/"
        >
          <ArrowLeft size={18} aria-hidden="true" />
          Voltar para o início
        </Link>
      </div>
    </main>
  );
}
