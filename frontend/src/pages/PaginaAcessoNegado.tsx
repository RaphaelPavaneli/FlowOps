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
    <main className="flex min-h-[calc(100vh-77px)] flex-col items-center justify-center bg-[radial-gradient(circle_at_50%_30%,rgba(191,219,254,0.4),transparent_27%),#f9fbff] px-6 py-12 text-center max-[700px]:min-h-[calc(100vh-116px)]">
      <span
        className="mb-[22px] grid size-[60px] place-items-center rounded-[18px] bg-[#fff1f0] text-[#b5473e]"
        aria-hidden="true"
      >
        <ShieldX size={30} />
      </span>
      <span className="mb-3.5 block text-[11px] font-[750] tracking-[0.11em] text-flowops-700 uppercase">
        Acesso restrito
      </span>
      <h1 className="m-0 max-w-[620px] text-[clamp(30px,4.5vw,45px)] leading-[1.14] tracking-[-1.6px] text-flowops-texto">
        Você não possui permissão para acessar esta página.
      </h1>
      <p className="mt-[17px] mb-7 max-w-[530px] text-[14px] leading-[1.7] text-flowops-cinza">
        Seu perfil continua autenticado, mas esta área exige outra permissão.
      </p>
      <Link
        className="inline-flex min-h-[46px] items-center justify-center gap-[9px] rounded-xl border border-transparent bg-[linear-gradient(110deg,#1d4ed8,#3b82f6)] px-5 text-[13.5px] font-bold text-white no-underline shadow-[0_12px_24px_rgba(37,99,235,0.2)] transition-[transform,box-shadow] duration-150 hover:-translate-y-px hover:shadow-[0_15px_30px_rgba(37,99,235,0.27)]"
        to={destino}
      >
        <ArrowLeft size={18} aria-hidden="true" />
        Voltar para minha área
      </Link>
    </main>
  );
}
