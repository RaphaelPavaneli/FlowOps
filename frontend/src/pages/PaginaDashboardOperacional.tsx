import { useEffect } from "react";
import {
  Activity,
  Bell,
  CheckCircle2,
  Clock3,
  Plus,
  ShieldCheck,
  Workflow,
  XCircle,
} from "lucide-react";
import { Link } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";

const recursosPlanejados = [
  {
    titulo: "Automações",
    descricao: "Quantidade de automações da sua operação.",
    Icone: Workflow,
  },
  {
    titulo: "Execuções recentes",
    descricao: "Histórico das execuções mais recentes.",
    Icone: Clock3,
  },
  {
    titulo: "Execuções com sucesso",
    descricao: "Automações concluídas sem falhas.",
    Icone: CheckCircle2,
  },
  {
    titulo: "Execuções com erro",
    descricao: "Falhas que precisam de acompanhamento.",
    Icone: XCircle,
  },
  {
    titulo: "Notificações recentes",
    descricao: "Avisos importantes sobre a sua operação.",
    Icone: Bell,
  },
];

function formatarPerfil(perfil: "administrador" | "usuario") {
  return perfil === "administrador" ? "Administrador" : "Usuário";
}

export function PaginaDashboardOperacional() {
  const { usuario } = useAutenticacao();

  useEffect(() => {
    document.title = "Dashboard | FlowOps";
  }, []);

  if (!usuario) {
    return null;
  }

  const administrador = usuario.perfil_acesso === "administrador";

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[radial-gradient(circle_at_88%_5%,rgba(191,219,254,0.38),transparent_28%),linear-gradient(155deg,#fff_0%,#f7faff_60%,#f8fafc_100%)] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] pt-16 pb-[84px] max-[700px]:w-[calc(100%_-_32px)] max-[700px]:pt-[46px] max-[700px]:pb-16">
        <section className="mb-[42px] flex items-end justify-between gap-10 max-[700px]:mb-[30px] max-[700px]:flex-col max-[700px]:items-start max-[700px]:gap-5">
          <div>
            <span className="mb-3.5 block text-[11px] font-[750] tracking-[0.11em] text-flowops-700 uppercase">
              Visão operacional
            </span>
            <h1 className="m-0 text-[clamp(36px,4.5vw,52px)] leading-[1.08] tracking-[-2px] text-flowops-texto max-[700px]:text-[36px] max-[700px]:tracking-[-1.4px]">
              Bem-vindo, {usuario.nome}
            </h1>
            <p className="mt-[13px] mb-0 max-w-[620px] text-[14.5px] leading-[1.7] text-flowops-cinza">
              Este será o ponto central para acompanhar automações, execuções e
              notificações da sua operação.
            </p>
          </div>
          <span className="inline-flex items-center gap-2 whitespace-nowrap rounded-[10px] border border-[#d7eadf] bg-[#f1fbf5] px-3 py-[9px] text-[10.5px] font-semibold text-[#347052]">
            <span className="size-1.5 rounded-full bg-[#34a476]" aria-hidden="true" />
            Sessão ativa · {formatarPerfil(usuario.perfil_acesso)}
          </span>
        </section>

        <section
          className="grid grid-cols-1 gap-[17px] min-[701px]:grid-cols-2 min-[1101px]:grid-cols-5"
          aria-label="Recursos planejados do dashboard operacional"
        >
          {recursosPlanejados.map(({ titulo, descricao, Icone }) => (
            <article
              className="rounded-[17px] border border-[#e3eaf4] bg-white/90 p-[23px] shadow-[0_12px_34px_rgba(30,64,175,0.05)]"
              key={titulo}
            >
              <span
                className="mb-[18px] grid size-[42px] place-items-center rounded-xl bg-flowops-50 text-flowops-700"
                aria-hidden="true"
              >
                <Icone size={21} />
              </span>
              <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
                Próxima etapa
              </span>
              <h2 className="mt-1.5 mb-0 text-[14px] text-[#283449]">{titulo}</h2>
              <p className="mt-2 mb-0 text-[11.5px] leading-[1.6] text-[#788599]">
                {descricao}
              </p>
            </article>
          ))}
        </section>

        <section className="mt-6 grid grid-cols-[auto_1fr] items-center gap-5 rounded-[19px] border border-[#dce7f6] bg-[radial-gradient(circle_at_95%_0%,rgba(191,219,254,0.42),transparent_42%),rgba(255,255,255,0.9)] p-[22px] shadow-[0_16px_44px_rgba(30,64,175,0.06)] min-[701px]:grid-cols-[auto_1fr_auto] min-[701px]:p-7">
          <div
            className="grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700"
            aria-hidden="true"
          >
            <Activity size={27} />
          </div>
          <div>
            <span className="text-[9.5px] font-[750] tracking-[0.08em] text-flowops-700 uppercase">
              Fundação preparada
            </span>
            <h2 className="mt-1 mb-0 text-[17px] text-[#283449]">
              As métricas serão conectadas a dados reais
            </h2>
            <p className="mt-[7px] mb-0 text-[12.5px] leading-[1.6] text-[#68758a]">
              O cadastro de automações será implementado antes dos indicadores,
              evitando números simulados no dashboard.
            </p>
          </div>
          <Link
            className="col-span-2 mt-1 inline-flex min-h-[46px] w-full items-center justify-center gap-[9px] rounded-xl border border-flowops-700 bg-flowops-700 px-5 text-[13.5px] font-bold text-white no-underline transition-colors hover:bg-flowops-800 min-[701px]:col-span-1 min-[701px]:mt-0 min-[701px]:w-auto"
            to="/app/automacoes"
          >
            <Plus size={18} aria-hidden="true" />
            Criar automação
          </Link>
        </section>

        {administrador && (
          <section className="mt-5 flex items-center justify-between gap-5 rounded-[15px] border border-[#e1e8f2] bg-white/75 px-5 py-4 max-[700px]:flex-col max-[700px]:items-start">
            <p className="m-0 inline-flex items-center gap-2 text-[12px] text-[#68758a]">
              <ShieldCheck className="text-flowops-600" size={17} aria-hidden="true" />
              Seu perfil também possui acesso aos indicadores administrativos.
            </p>
            <Link
              className="text-[12px] font-bold text-flowops-700 no-underline hover:underline hover:underline-offset-[3px]"
              to="/app/administracao/dashboard"
            >
              Abrir visão administrativa
            </Link>
          </section>
        )}
      </div>
    </main>
  );
}
