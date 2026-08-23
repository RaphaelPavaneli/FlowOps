import { useEffect } from "react";
import {
  BadgeCheck,
  Mail,
  ShieldCheck,
  UserRound,
} from "lucide-react";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";

function formatarPerfil(perfil: "administrador" | "usuario") {
  return perfil === "administrador" ? "Administrador" : "Usuário";
}

export function PaginaMinhaConta() {
  const { usuario } = useAutenticacao();

  useEffect(() => {
    document.title = "Minha conta | FlowOps";
  }, []);

  if (!usuario) {
    return null;
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_82%_12%,rgba(191,219,254,0.42),transparent_27%),linear-gradient(145deg,#fff,#f7faff)]">
      <div className="mx-auto grid min-h-[calc(100vh-77px)] w-[calc(100%_-_48px)] max-w-[1160px] grid-cols-[minmax(0,0.9fr)_minmax(420px,1.1fr)] items-center gap-[clamp(60px,9vw,130px)] py-[70px] max-[960px]:grid-cols-1 max-[960px]:content-center max-[960px]:gap-12 max-[700px]:min-h-[calc(100vh-69px)] max-[700px]:w-[calc(100%_-_32px)] max-[700px]:py-[52px]">
        <section
          className="max-[960px]:mx-auto max-[960px]:max-w-[680px] max-[960px]:text-center"
          aria-labelledby="titulo-area"
        >
          <span className="mb-[22px] inline-flex items-center gap-[7px] rounded-full border border-[#d9e7fb] bg-[rgba(242,247,255,0.86)] px-3 py-[7px] text-[11px] font-[750] tracking-[0.08em] text-[#315a9f] uppercase">
            <ShieldCheck size={15} aria-hidden="true" />
            Sessão protegida
          </span>
          <h1
            className="m-0 max-w-[560px] text-[clamp(38px,5vw,58px)] leading-[1.06] tracking-[-2.2px] text-flowops-texto max-[700px]:text-[38px] max-[700px]:tracking-[-1.5px]"
            id="titulo-area"
          >
            Bem-vindo, {usuario.nome}
          </h1>
          <p className="mt-[21px] mb-0 max-w-[520px] text-[16px] leading-[1.75] text-flowops-cinza max-[960px]:mx-auto max-[700px]:text-[14.5px]">
            Sua identidade foi validada pelo backend e sua sessão está ativa
            nesta aba.
          </p>
        </section>

        <section
          className="rounded-[22px] border border-white/95 bg-white/85 p-[30px] shadow-[0_26px_70px_rgba(30,64,175,0.1),0_8px_24px_rgba(15,23,42,0.05)] backdrop-blur-[14px] max-[960px]:mx-auto max-[960px]:w-full max-[960px]:max-w-[620px] max-[700px]:rounded-[18px] max-[700px]:p-[22px]"
          aria-labelledby="titulo-sessao"
        >
          <div className="grid grid-cols-[auto_1fr_auto] items-center gap-3.5 border-b border-[#e8edf4] pb-6 max-[700px]:grid-cols-[auto_1fr]">
            <div
              className="grid size-[46px] place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
              aria-hidden="true"
            >
              <UserRound size={24} />
            </div>
            <div className="flex flex-col gap-1">
              <span className="text-[10.5px] font-[650] tracking-[0.06em] text-[#7c899c] uppercase">
                Usuário autenticado
              </span>
              <h2 className="m-0 text-[16px]" id="titulo-sessao">
                Informações da sua conta
              </h2>
            </div>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-[#ecfdf5] px-[9px] py-1.5 text-[10.5px] font-[650] text-[#287355] max-[700px]:col-span-2 max-[700px]:justify-self-start">
              <span className="size-1.5 rounded-full bg-[#34a476]" aria-hidden="true" />
              Ativa
            </span>
          </div>

          <dl className="mt-6 mb-0 grid gap-[13px]">
            <div className="rounded-[13px] border border-[#e6ebf3] bg-[#fbfdff] p-[17px]">
              <dt className="flex items-center gap-[7px] text-[11.5px] text-[#7a8799]">
                <Mail className="text-flowops-600" size={17} aria-hidden="true" />
                E-mail
              </dt>
              <dd className="mt-2 mb-0 text-[14px] font-[650] text-[#283449]">
                {usuario.email}
              </dd>
            </div>
            <div className="rounded-[13px] border border-[#e6ebf3] bg-[#fbfdff] p-[17px]">
              <dt className="flex items-center gap-[7px] text-[11.5px] text-[#7a8799]">
                <BadgeCheck className="text-flowops-600" size={17} aria-hidden="true" />
                Perfil
              </dt>
              <dd className="mt-2 mb-0 text-[14px] font-[650] text-[#283449]">
                {formatarPerfil(usuario.perfil_acesso)}
              </dd>
            </div>
          </dl>
        </section>
      </div>
    </main>
  );
}
