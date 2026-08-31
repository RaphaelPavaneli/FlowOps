import { useEffect } from "react";
import {
  ArrowLeft,
  ArrowRight,
  BadgeCheck,
  ChartNoAxesCombined,
  LockKeyhole,
  Network,
  Settings2,
  UsersRound,
} from "lucide-react";
import { Link } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";

export function PaginaAdministracao() {
  const { usuario } = useAutenticacao();

  useEffect(() => {
    document.title = "Administração | FlowOps";
  }, []);

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[radial-gradient(circle_at_88%_5%,rgba(191,219,254,0.38),transparent_28%),linear-gradient(155deg,#fff_0%,#f7faff_60%,#f8fafc_100%)] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] pt-16 pb-[84px] max-[700px]:w-[calc(100%_-_32px)] max-[700px]:pt-[46px] max-[700px]:pb-16">
        <Link
          className="mb-9 inline-flex items-center gap-[7px] text-[12px] font-[650] text-flowops-700 no-underline hover:underline hover:underline-offset-[3px]"
          to="/app/dashboard"
        >
          <ArrowLeft size={17} aria-hidden="true" />
          Voltar ao dashboard
        </Link>

        <section className="mb-[42px] flex items-start gap-[18px] max-[700px]:flex-col">
          <span
            className="grid size-[52px] shrink-0 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
            aria-hidden="true"
          >
            <Settings2 size={25} />
          </span>
          <div>
            <span className="mb-3.5 block text-[11px] font-[750] tracking-[0.11em] text-flowops-700 uppercase">
              Área exclusiva
            </span>
            <h1 className="m-0 text-[clamp(36px,4.5vw,52px)] leading-[1.08] tracking-[-2px] text-flowops-texto max-[700px]:text-[36px] max-[700px]:tracking-[-1.4px]">
              Administração
            </h1>
            <p className="mt-[13px] mb-0 text-[14.5px] leading-[1.7] text-flowops-cinza">
              Gerencie os recursos administrativos disponíveis no FlowOps.
            </p>
          </div>
        </section>

        <section className="grid grid-cols-[1.15fr_0.85fr] gap-5 max-[960px]:grid-cols-1">
          <article className="relative rounded-[19px] border border-[#e1e8f2] bg-white/90 p-7 shadow-[0_14px_40px_rgba(30,64,175,0.05)] max-[700px]:p-[23px]">
            <span
              className="mb-[22px] grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
              aria-hidden="true"
            >
              <ChartNoAxesCombined size={23} />
            </span>
            <div>
              <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
                Visão geral
              </span>
              <h2 className="mt-1 mb-0 text-[17px] text-[#283449]">
                Dashboard administrativo
              </h2>
              <p className="mt-[7px] mb-0 text-[12.5px] leading-[1.6] text-[#68758a]">
                Acompanhe os indicadores globais de usuários da plataforma.
              </p>
            </div>
            <Link
              className="mt-6 inline-flex min-h-[44px] items-center justify-center gap-2 rounded-[11px] bg-[linear-gradient(110deg,#1d4ed8,#3b82f6)] px-[18px] text-[12.5px] font-bold text-white no-underline shadow-[0_10px_22px_rgba(37,99,235,0.18)] transition-[transform,box-shadow] hover:-translate-y-px hover:shadow-[0_13px_27px_rgba(37,99,235,0.25)]"
              to="/app/administracao/dashboard"
            >
              Acessar indicadores
              <ArrowRight size={17} aria-hidden="true" />
            </Link>
          </article>

          <article className="relative rounded-[19px] border border-[#e1e8f2] bg-white/90 p-7 shadow-[0_14px_40px_rgba(30,64,175,0.05)] max-[700px]:p-[23px]">
            <span
              className="mb-[22px] grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
              aria-hidden="true"
            >
              <UsersRound size={23} />
            </span>
            <div>
              <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
                Gestão de acesso
              </span>
              <h2 className="mt-1 mb-0 text-[17px] text-[#283449]">
                Gerenciamento de usuários
              </h2>
              <p className="mt-[7px] mb-0 text-[12.5px] leading-[1.6] text-[#68758a]">
                Gerencie perfis, permissões e o estado das contas da plataforma.
              </p>
            </div>
            <Link
              className="mt-6 inline-flex min-h-[44px] items-center justify-center gap-2 rounded-[11px] bg-[linear-gradient(110deg,#1d4ed8,#3b82f6)] px-[18px] text-[12.5px] font-bold text-white no-underline shadow-[0_10px_22px_rgba(37,99,235,0.18)] transition-[transform,box-shadow] hover:-translate-y-px hover:shadow-[0_13px_27px_rgba(37,99,235,0.25)]"
              to="/app/administracao/usuarios"
            >
              Acessar usuários
              <ArrowRight size={17} aria-hidden="true" />
            </Link>
          </article>

          <article className="relative rounded-[19px] border border-[#e1e8f2] bg-white/90 p-7 shadow-[0_14px_40px_rgba(30,64,175,0.05)] max-[700px]:p-[23px]">
            <span
              className="mb-[22px] grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
              aria-hidden="true"
            >
              <Network size={23} />
            </span>
            <div>
              <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
                Organização operacional
              </span>
              <h2 className="mt-1 mb-0 text-[17px] text-[#283449]">
                Gestão de equipes
              </h2>
              <p className="mt-[7px] mb-0 text-[12.5px] leading-[1.6] text-[#68758a]">
                Crie equipes e associe os usuários aos seus grupos de trabalho.
              </p>
            </div>
            <Link
              className="mt-6 inline-flex min-h-[44px] items-center justify-center gap-2 rounded-[11px] bg-[linear-gradient(110deg,#1d4ed8,#3b82f6)] px-[18px] text-[12.5px] font-bold text-white no-underline shadow-[0_10px_22px_rgba(37,99,235,0.18)] transition-[transform,box-shadow] hover:-translate-y-px hover:shadow-[0_13px_27px_rgba(37,99,235,0.25)]"
              to="/app/administracao/equipes"
            >
              Acessar equipes
              <ArrowRight size={17} aria-hidden="true" />
            </Link>
          </article>

          <article className="rounded-[19px] border border-[#e1e8f2] bg-white/90 p-7 shadow-[0_14px_40px_rgba(30,64,175,0.05)] max-[700px]:p-[23px]">
            <div className="flex items-center gap-[13px] border-b border-[#e8edf4] pb-5">
              <span
                className="grid size-[42px] place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
                aria-hidden="true"
              >
                <LockKeyhole size={21} />
              </span>
              <div>
                <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
                  Sessão atual
                </span>
                <h2 className="mt-1 mb-0 text-[17px] text-[#283449]">
                  Administrador autenticado
                </h2>
              </div>
            </div>
            <dl className="mt-5 mb-0 grid gap-[13px]">
              <div className="flex items-center justify-between gap-5">
                <dt className="text-[11px] text-[#7c899c]">Nome</dt>
                <dd className="m-0 inline-flex max-w-[70%] items-center gap-[5px] overflow-hidden text-ellipsis whitespace-nowrap text-[11.5px] font-[650] text-[#344055]">
                  {usuario?.nome}
                </dd>
              </div>
              <div className="flex items-center justify-between gap-5">
                <dt className="text-[11px] text-[#7c899c]">E-mail</dt>
                <dd className="m-0 inline-flex max-w-[70%] items-center gap-[5px] overflow-hidden text-ellipsis whitespace-nowrap text-[11.5px] font-[650] text-[#344055]">
                  {usuario?.email}
                </dd>
              </div>
              <div className="flex items-center justify-between gap-5">
                <dt className="text-[11px] text-[#7c899c]">Perfil</dt>
                <dd className="m-0 inline-flex max-w-[70%] items-center gap-[5px] overflow-hidden text-ellipsis whitespace-nowrap text-[11.5px] font-[650] text-[#344055]">
                  <BadgeCheck className="text-flowops-600" size={15} aria-hidden="true" />
                  Administrador
                </dd>
              </div>
            </dl>
          </article>
        </section>
      </div>
    </main>
  );
}
