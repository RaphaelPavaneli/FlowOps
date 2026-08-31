import { useEffect } from "react";

import { FormularioCadastro } from "../components/FormularioCadastro";
import { Marca } from "../components/Marca";

export function PaginaCadastro() {
  useEffect(() => {
    document.title = "Criar conta | FlowOps";
  }, []);

  return (
    <main className="relative isolate grid min-h-screen grid-rows-[auto_1fr_auto] overflow-x-hidden bg-[radial-gradient(circle_at_77%_15%,rgba(191,219,254,0.48),transparent_28%),radial-gradient(circle_at_16%_86%,rgba(224,231,255,0.58),transparent_27%),linear-gradient(145deg,#fbfdff_0%,#f7f9fc_50%,#f9fafc_100%)]">
      <div
        className="pointer-events-none absolute -top-35 right-[6%] z-0 size-[470px] rounded-full bg-blue-300/17 blur-[18px]"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute -bottom-52.5 -left-22.5 z-0 size-[500px] rounded-full bg-indigo-300/16 blur-[20px]"
        aria-hidden="true"
      />

      <header className="relative z-3 px-6 py-6 sm:px-[clamp(1.5rem,6vw,5.5rem)] sm:py-8">
        <Marca />
      </header>

      <section
        className="relative z-2 flex w-full items-start justify-center px-4 pt-2 pb-9 sm:px-6 sm:pt-0 sm:pb-12"
        aria-labelledby="titulo-cadastro"
      >
        <FormularioCadastro />
      </section>

      <footer className="relative z-2 px-6 pt-5 pb-7 text-center text-[11.5px] text-[#8a95a7]">
        © {new Date().getFullYear()} FlowOps. Gestão que flui com você.
      </footer>
    </main>
  );
}
