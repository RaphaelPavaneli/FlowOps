import { useEffect } from "react";

import { FormularioLogin } from "../components/FormularioLogin";
import { Marca } from "../components/Marca";

export function PaginaLogin() {
  useEffect(() => {
    document.title = "Entrar | FlowOps";
  }, []);

  return (
    <main className="relative isolate grid min-h-screen grid-rows-[auto_1fr_auto] overflow-hidden bg-[radial-gradient(circle_at_77%_15%,rgba(191,219,254,0.48),transparent_28%),radial-gradient(circle_at_16%_86%,rgba(224,231,255,0.58),transparent_27%),linear-gradient(145deg,#fbfdff_0%,#f7f9fc_50%,#f9fafc_100%)]">
      <div
        className="pointer-events-none absolute -top-35 right-[6%] z-0 size-[470px] rounded-full bg-blue-300/17 blur-[18px]"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute -bottom-52.5 -left-22.5 z-0 size-[500px] rounded-full bg-indigo-300/16 blur-[20px]"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute top-16.5 -right-45 z-0 h-34 w-[330px] rotate-[-8deg] rounded-l-[80px] border border-r-0 border-[rgba(105,144,224,0.22)] shadow-[inset_0_0_50px_rgba(191,219,254,0.14)] sm:-right-15"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute bottom-[8%] -left-47.5 z-0 h-30 w-72.5 rotate-[7deg] rounded-r-[70px] border border-l-0 border-[rgba(105,144,224,0.22)] after:absolute after:-top-8.5 after:-right-7.5 after:size-2.5 after:rounded-full after:border-[3px] after:border-[rgba(68,113,204,0.32)] after:content-[''] sm:-left-26.25"
        aria-hidden="true"
      />

      <header className="relative z-3 px-6 py-6 sm:px-[clamp(1.5rem,6vw,5.5rem)] sm:py-8">
        <Marca />
      </header>

      <section
        className="relative z-2 flex w-full items-start justify-center px-4 pt-7 pb-9 sm:items-center sm:px-6 sm:pt-4 sm:pb-12"
        aria-labelledby="titulo-login"
      >
        <FormularioLogin />
      </section>

      <footer className="relative z-2 px-6 pt-5 pb-7 text-center text-[11.5px] text-[#8a95a7]">
        © {new Date().getFullYear()} FlowOps. Gestão que flui com você.
      </footer>
    </main>
  );
}
