import { useCallback, useEffect, useState } from "react";
import {
  ArrowRight,
  CircleGauge,
  RefreshCw,
  ShieldCheck,
  UserCheck,
  UserRound,
  UserRoundCog,
  UsersRound,
  UserX,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import {
  ErroDashboard,
  obterResumoDashboardAdministrativo,
} from "../services/dashboard";
import type { ResumoDashboardAdministrativo } from "../types/dashboard";

const classesEstadoDashboard =
  "flex min-h-[270px] flex-col items-center justify-center gap-3.5 rounded-[18px] border border-[#e1e8f2] bg-white/80 p-9 text-center text-flowops-cinza";

export function PaginaDashboardAdministrativo() {
  const { token, usuario, sair } = useAutenticacao();
  const navegar = useNavigate();
  const [resumo, setResumo] = useState<ResumoDashboardAdministrativo | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    document.title = "Dashboard administrativo | FlowOps";
  }, []);

  const carregarResumo = useCallback(async () => {
    if (!token) {
      return;
    }

    setCarregando(true);
    setErro("");

    try {
      setResumo(await obterResumoDashboardAdministrativo(token));
    } catch (falha) {
      if (falha instanceof ErroDashboard && falha.status === 401) {
        sair();
        return;
      }

      if (falha instanceof ErroDashboard && falha.status === 403) {
        navegar("/app/acesso-negado", { replace: true });
        return;
      }

      setErro(
        falha instanceof ErroDashboard
          ? falha.message
          : "Ocorreu um erro inesperado ao carregar o dashboard.",
      );
    } finally {
      setCarregando(false);
    }
  }, [token, navegar, sair]);

  useEffect(() => {
    void carregarResumo();
  }, [carregarResumo]);

  const metricas = resumo
    ? [
        { titulo: "Total de usuários", valor: resumo.usuarios.total, Icone: UsersRound },
        { titulo: "Usuários ativos", valor: resumo.usuarios.ativos, Icone: UserCheck },
        { titulo: "Usuários inativos", valor: resumo.usuarios.inativos, Icone: UserX },
        { titulo: "Administradores", valor: resumo.usuarios.administradores, Icone: ShieldCheck },
        { titulo: "Usuários comuns", valor: resumo.usuarios.comuns, Icone: UserRound },
      ]
    : [];

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[radial-gradient(circle_at_88%_5%,rgba(191,219,254,0.38),transparent_28%),linear-gradient(155deg,#fff_0%,#f7faff_60%,#f8fafc_100%)] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] pt-16 pb-[84px] max-[700px]:w-[calc(100%_-_32px)] max-[700px]:pt-[46px] max-[700px]:pb-16">
        <section className="mb-[42px] flex items-end justify-between gap-10 max-[700px]:mb-[30px] max-[700px]:flex-col max-[700px]:items-start max-[700px]:gap-5">
          <div>
            <span className="mb-3.5 block text-[11px] font-[750] tracking-[0.11em] text-flowops-700 uppercase">
              Visão geral
            </span>
            <h1 className="m-0 text-[clamp(36px,4.5vw,52px)] leading-[1.08] tracking-[-2px] text-flowops-texto max-[700px]:text-[36px] max-[700px]:tracking-[-1.4px]">
              Bem-vindo, {usuario?.nome}
            </h1>
            <p className="mt-[13px] mb-0 text-[14.5px] leading-[1.7] text-flowops-cinza">
              Acompanhe os principais indicadores de usuários da plataforma.
            </p>
          </div>
          <span className="inline-flex items-center gap-2 whitespace-nowrap rounded-[10px] border border-[#dde7f5] bg-white/75 px-3 py-[9px] text-[10.5px] font-semibold text-[#607087]">
            <CircleGauge className="text-flowops-600" size={18} aria-hidden="true" />
            Dados atualizados pelo FlowOps
          </span>
        </section>

        {carregando && (
          <section
            className={classesEstadoDashboard}
            aria-live="polite"
            aria-busy="true"
          >
            <span
              className="size-6 animate-spin rounded-full border-2 border-flowops-600/20 border-t-flowops-600"
              aria-hidden="true"
            />
            <p className="m-0 text-[13px]">Carregando informações do dashboard...</p>
          </section>
        )}

        {!carregando && erro && (
          <section
            className={`${classesEstadoDashboard} bg-[rgba(255,250,250,0.88)] text-[#8f3029]`}
            role="alert"
          >
            <p className="m-0 text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-[46px] cursor-pointer items-center justify-center gap-[9px] rounded-xl border border-[#cfddf4] bg-white px-5 text-[13.5px] font-bold text-flowops-700 transition-[transform,box-shadow,color,border-color,background] duration-150 hover:-translate-y-px hover:border-[#aac5ef] hover:bg-flowops-50"
              type="button"
              onClick={carregarResumo}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resumo && (
          <>
            <section
              className="grid grid-cols-1 gap-[17px] min-[701px]:grid-cols-2 min-[1101px]:grid-cols-5"
              aria-label="Resumo de usuários"
            >
              {metricas.map(({ titulo, valor, Icone }) => (
                <article
                  className="grid grid-cols-[auto_1fr] items-center gap-x-[13px] gap-y-[5px] rounded-[17px] border border-[#e3eaf4] bg-white/90 p-[23px] shadow-[0_12px_34px_rgba(30,64,175,0.05)]"
                  key={titulo}
                >
                  <span className="row-span-2 grid size-[42px] place-items-center rounded-xl bg-flowops-50 text-flowops-700">
                    <Icone size={21} />
                  </span>
                  <span className="text-[10.5px] font-semibold text-[#788599]">
                    {titulo}
                  </span>
                  <strong className="text-[24px] tracking-[-0.8px] text-flowops-900">
                    {valor}
                  </strong>
                </article>
              ))}
            </section>

            <section className="mt-6 grid grid-cols-[auto_1fr] items-center gap-5 rounded-[19px] border border-[#dce7f6] bg-[radial-gradient(circle_at_95%_0%,rgba(191,219,254,0.42),transparent_42%),rgba(255,255,255,0.9)] p-[22px] shadow-[0_16px_44px_rgba(30,64,175,0.06)] min-[701px]:grid-cols-[auto_1fr_auto] min-[701px]:p-7">
              <div
                className="grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
                aria-hidden="true"
              >
                <UserRoundCog size={27} />
              </div>
              <div>
                <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
                  Área exclusiva
                </span>
                <h2 className="mt-1 mb-0 text-[17px] text-[#283449]">Gerenciamento de usuários</h2>
                <p className="mt-[7px] mb-0 text-[12.5px] leading-[1.6] text-[#68758a]">
                  Gerencie perfis, permissões e o estado das contas da plataforma.
                </p>
              </div>
              <Link
                className="col-span-2 mt-1 inline-flex min-h-[46px] w-full items-center justify-center gap-[9px] rounded-xl border border-transparent bg-[linear-gradient(110deg,#1d4ed8,#3b82f6)] px-5 text-[13.5px] font-bold text-white no-underline shadow-[0_12px_24px_rgba(37,99,235,0.2)] transition-[transform,box-shadow] duration-150 hover:-translate-y-px hover:shadow-[0_15px_30px_rgba(37,99,235,0.27)] min-[701px]:col-span-1 min-[701px]:mt-0 min-[701px]:w-auto"
                to="/app/administracao/usuarios"
              >
                Acessar
                <ArrowRight size={18} aria-hidden="true" />
              </Link>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
