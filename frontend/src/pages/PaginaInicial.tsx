import { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  ArrowRight,
  CheckCircle2,
  Clock3,
  History,
  LockKeyhole,
  Pause,
  Play,
  ShieldCheck,
  UsersRound,
  Workflow,
} from "lucide-react";

import { Marca } from "../components/Marca";

const etapas = [
  ["1", "Crie sua conta", "O cadastro cria um usuário comum."],
  ["2", "Entre em uma equipe", "Um administrador faz a associação."],
  ["3", "Cadastre a automação", "O registro começa como rascunho."],
  ["4", "Execute e acompanhe", "Ative, execute, pause e consulte o histórico."],
] as const;

const automacoesDemonstracao = [
  ["Teste controlado — sucesso", "Ativa", "Concluída", "1 min 02 s", true],
  ["Teste controlado — falha", "Pausada", "Falhou", "1 min 00 s", false],
  ["Validação de cancelamento", "Ativa", "Cancelada", "18 s", true],
  ["Automação em rascunho", "Rascunho", "Nunca executada", "—", false],
  ["Teste de concorrência", "Ativa", "Concluída", "1 min 01 s", true],
] as const;

const capacidades = [
  {
    titulo: "Catálogo compartilhado",
    descricao:
      "As automações ficam disponíveis para os integrantes da mesma equipe, sem misturar contextos.",
    Icone: Workflow,
  },
  {
    titulo: "Execução acompanhável",
    descricao:
      "Acompanhe estados, duração, falhas e cancelamentos sem sair da listagem operacional.",
    Icone: Clock3,
  },
  {
    titulo: "Histórico rastreável",
    descricao:
      "Consulte cada execução, seus horários e o resultado persistido para a automação.",
    Icone: History,
  },
  {
    titulo: "Administração controlada",
    descricao:
      "Administradores gerenciam usuários, equipes, perfis e situação das contas.",
    Icone: UsersRound,
  },
];

const tecnologias = [
  "React + TypeScript",
  "FastAPI + Python",
  "SQLAlchemy + SQL Server",
  "Pytest + GitHub Actions",
];

const classesStatus: Record<string, string> = {
  Ativa: "bg-[#e9f8ef] text-[#1f7644]",
  Pausada: "bg-[#fff4db] text-[#8a6218]",
  Rascunho: "bg-[#eef1f5] text-[#5f6c80]",
};

const classesExecucao: Record<string, string> = {
  "Concluída": "text-[#237a45]",
  Falhou: "text-[#a13a32]",
  Cancelada: "text-[#8a6218]",
  "Nunca executada": "text-[#7a8799]",
};

export function PaginaInicial() {
  useEffect(() => {
    document.title = "FlowOps | Automações compartilhadas por equipe";
  }, []);

  return (
    <div className="min-h-screen bg-white text-flowops-texto">
      <a
        className="fixed top-3 left-3 z-100 -translate-y-[160%] rounded-lg bg-flowops-700 px-3.5 py-2.5 text-sm font-semibold text-white no-underline transition-transform duration-150 focus:translate-y-0"
        href="#conteudo-principal"
      >
        Ir para o conteúdo principal
      </a>

      <header className="sticky top-0 z-40 border-b border-[#dde5ef] bg-white/96 backdrop-blur-md">
        <div className="mx-auto flex min-h-18 w-[min(calc(100%_-_2rem),1440px)] items-center justify-between gap-6 sm:w-[min(calc(100%_-_4rem),1440px)]">
          <Marca />

          <nav className="hidden items-center gap-7 lg:flex" aria-label="Navegação principal">
            <a className="text-[13px] font-semibold text-flowops-cinza no-underline hover:text-flowops-700" href="#produto">Produto</a>
            <a className="text-[13px] font-semibold text-flowops-cinza no-underline hover:text-flowops-700" href="#como-funciona">Como funciona</a>
            <a className="text-[13px] font-semibold text-flowops-cinza no-underline hover:text-flowops-700" href="#seguranca">Segurança</a>
            <a className="text-[13px] font-semibold text-flowops-cinza no-underline hover:text-flowops-700" href="#tecnologia">Tecnologia</a>
          </nav>

          <div className="flex items-center gap-2.5">
            <Link className="hidden min-h-10 items-center px-2 text-[13px] font-bold text-flowops-700 no-underline hover:text-flowops-900 sm:inline-flex" to="/login">
              Entrar
            </Link>
            <Link className="inline-flex min-h-10 items-center justify-center gap-2 rounded-lg bg-flowops-700 px-4 text-[13px] font-bold text-white no-underline hover:bg-flowops-900" to="/cadastro">
              Criar conta
              <ArrowRight size={16} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </header>

      <main id="conteudo-principal">
        <section className="border-b border-[#dce6f1] bg-flowops-app py-16 sm:py-20" id="produto">
          <div className="mx-auto grid w-[min(calc(100%_-_2rem),1440px)] items-center gap-12 sm:w-[min(calc(100%_-_4rem),1440px)] lg:grid-cols-[0.82fr_1.18fr]">
            <div className="max-w-160">
              <span className="inline-flex rounded-full border border-[#cbdcf1] bg-white px-3 py-1.5 text-[10px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
                MVP full-stack
              </span>
              <h1 className="mt-5 mb-0 text-[clamp(2.5rem,6vw,4rem)] leading-[1.04] font-bold tracking-[-0.045em] text-flowops-texto">
                Automações da sua equipe, organizadas e acompanhadas em um só lugar.
              </h1>
              <p className="mt-6 mb-0 max-w-150 text-[clamp(1rem,1.8vw,1.125rem)] leading-7 text-flowops-cinza">
                Cadastre automações, acompanhe execuções e consulte o histórico com isolamento por equipe.
              </p>

              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Link className="inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-flowops-700 px-5 text-[13px] font-bold text-white no-underline hover:bg-flowops-900" to="/login">
                  Acessar plataforma
                  <ArrowRight size={17} aria-hidden="true" />
                </Link>
                <a className="inline-flex min-h-11 items-center justify-center rounded-lg border border-[#c9d7e8] bg-white px-5 text-[13px] font-bold text-flowops-700 no-underline hover:bg-flowops-50" href="#como-funciona">
                  Conhecer o projeto
                </a>
              </div>

              <p className="mt-6 mb-0 flex items-start gap-2 text-xs leading-5 text-[#69768a]">
                <ShieldCheck className="mt-0.5 shrink-0 text-flowops-600" size={16} aria-hidden="true" />
                Catálogo compartilhado, execução controlada e histórico persistido para cada equipe.
              </p>
            </div>

            <PreviewProduto />
          </div>
        </section>

        <section className="py-16 sm:py-20" id="como-funciona">
          <div className="mx-auto w-[min(calc(100%_-_2rem),1440px)] sm:w-[min(calc(100%_-_4rem),1440px)]">
            <span className="text-[10px] font-bold tracking-[0.1em] text-flowops-700 uppercase">Como funciona</span>
            <h2 className="mt-3 mb-0 max-w-150 text-[clamp(1.875rem,4vw,2.5rem)] leading-tight tracking-[-0.035em]">
              Um fluxo simples, com responsabilidades claras.
            </h2>

            <ol className="mt-10 grid list-none gap-8 p-0 sm:grid-cols-2 lg:grid-cols-4 lg:gap-5">
              {etapas.map(([numero, titulo, descricao], indice) => (
                <li className="relative grid grid-cols-[44px_1fr] gap-3 lg:grid-cols-1" key={numero}>
                  <span className="grid size-11 place-items-center rounded-full bg-flowops-50 text-sm font-bold text-flowops-700">{numero}</span>
                  {indice < etapas.length - 1 && (
                    <span className="absolute top-5.5 left-13 hidden h-px w-[calc(100%_-_3.75rem)] border-t border-dashed border-[#c9d9ec] lg:block" aria-hidden="true" />
                  )}
                  <div className="lg:mt-4">
                    <h3 className="m-0 text-[15px] font-bold">{titulo}</h3>
                    <p className="mt-2 mb-0 text-[13px] leading-5 text-flowops-cinza">{descricao}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="border-y border-[#dfe7f0] bg-[#f8fafc] py-16 sm:py-20">
          <div className="mx-auto grid w-[min(calc(100%_-_2rem),1440px)] gap-10 sm:w-[min(calc(100%_-_4rem),1440px)] lg:grid-cols-[0.72fr_1.28fr] lg:gap-30">
            <div>
              <span className="text-[10px] font-bold tracking-[0.1em] text-flowops-700 uppercase">Capacidades do MVP</span>
              <h2 className="mt-3 mb-0 text-[clamp(1.875rem,4vw,2.5rem)] leading-tight tracking-[-0.035em]">
                O necessário para operar e demonstrar o fluxo completo.
              </h2>
              <p className="mt-5 mb-0 text-sm leading-6 text-flowops-cinza">
                O FlowOps mantém o escopo propositalmente objetivo: organizar automações da equipe e acompanhar execuções controladas com segurança.
              </p>
            </div>

            <div className="grid border-t border-[#d8e1ec] sm:grid-cols-2">
              {capacidades.map(({ titulo, descricao, Icone }, indice) => (
                <article className={`border-b border-[#d8e1ec] py-8 sm:px-8 ${indice % 2 === 0 ? "sm:border-r" : ""}`} key={titulo}>
                  <Icone className="text-flowops-700" size={20} strokeWidth={1.8} aria-hidden="true" />
                  <h3 className="mt-4 mb-0 text-[15px] font-bold">{titulo}</h3>
                  <p className="mt-2 mb-0 text-[13px] leading-5 text-flowops-cinza">{descricao}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-flowops-sidebar-top py-16 text-white sm:py-20" id="seguranca">
          <div className="mx-auto grid w-[min(calc(100%_-_2rem),1440px)] items-start gap-10 sm:w-[min(calc(100%_-_4rem),1440px)] lg:grid-cols-[0.9fr_1.1fr] lg:gap-20">
            <div>
              <span className="text-[10px] font-bold tracking-[0.1em] text-[#8ebfff] uppercase">Segurança por padrão</span>
              <h2 className="mt-3 mb-0 text-[clamp(1.875rem,4vw,2.5rem)] leading-tight tracking-[-0.035em]">
                A equipe não é escolhida pelo cliente.
              </h2>
              <p className="mt-5 mb-0 max-w-130 text-sm leading-6 text-[#b8c8db]">
                O backend recarrega o usuário autenticado, resolve sua equipe ativa e aplica esse contexto em consultas e gravações.
              </p>
            </div>

            <ul className="m-0 grid list-none border-t border-white/15 p-0">
              {[
                "Senhas protegidas com Argon2id.",
                "Sessão autenticada com JWT e revalidação do usuário.",
                "Cadastro público sem escolha de perfil ou equipe.",
                "Dados de automações e execuções isolados por equipe.",
              ].map((item) => (
                <li className="flex items-center gap-3 border-b border-white/15 py-4 text-sm text-[#dbe7f5]" key={item}>
                  <CheckCircle2 className="shrink-0 text-[#75aefa]" size={18} aria-hidden="true" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="py-16 sm:py-20" id="tecnologia">
          <div className="mx-auto w-[min(calc(100%_-_2rem),1440px)] sm:w-[min(calc(100%_-_4rem),1440px)]">
            <div className="grid items-center gap-8 border-b border-[#dce5ef] pb-10 lg:grid-cols-[0.8fr_1.2fr]">
              <div>
                <span className="text-[10px] font-bold tracking-[0.1em] text-flowops-700 uppercase">MVP full-stack</span>
                <h2 className="mt-3 mb-0 text-[clamp(1.875rem,4vw,2.5rem)] leading-tight tracking-[-0.035em]">
                  Produto funcional, arquitetura demonstrável.
                </h2>
              </div>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                {tecnologias.map((tecnologia) => (
                  <span className="flex min-h-16 items-center justify-center rounded-lg border border-[#dce5ef] bg-[#fbfcfe] px-4 text-center text-[13px] font-semibold text-[#3e4b60]" key={tecnologia}>
                    {tecnologia}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-8 flex items-start gap-3 rounded-lg border border-[#dbe5f0] bg-flowops-50 px-4 py-3 text-[13px] leading-5 text-[#526077]">
              <LockKeyhole className="mt-0.5 shrink-0 text-flowops-700" size={18} aria-hidden="true" />
              <p className="m-0">
                O executor atual processa cenários controlados em uma única instância. Integrações externas e filas distribuídas permanecem no roadmap.
              </p>
            </div>
          </div>
        </section>

        <section className="border-t border-[#dfe7f0] bg-flowops-app py-16 sm:py-20">
          <div className="mx-auto flex w-[min(calc(100%_-_2rem),860px)] flex-col items-center text-center sm:w-[min(calc(100%_-_3rem),860px)]">
            <h2 className="m-0 text-[clamp(1.875rem,4vw,2.5rem)] leading-tight tracking-[-0.035em]">Conheça o fluxo completo do FlowOps.</h2>
            <p className="mt-4 mb-0 max-w-150 text-sm leading-6 text-flowops-cinza">
              Entre com sua conta ou faça um cadastro como usuário comum para conhecer a experiência do MVP.
            </p>
            <div className="mt-7 flex flex-col gap-3 sm:flex-row">
              <Link className="inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-flowops-700 px-5 text-[13px] font-bold text-white no-underline hover:bg-flowops-900" to="/login">
                Acessar plataforma
                <ArrowRight size={17} aria-hidden="true" />
              </Link>
              <a className="inline-flex min-h-11 items-center justify-center rounded-lg border border-[#c9d7e8] bg-white px-5 text-[13px] font-bold text-flowops-700 no-underline hover:bg-flowops-50" href="https://github.com/RaphaelPavaneli/FlowOps" rel="noreferrer" target="_blank">
                Ver no GitHub
              </a>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-[#dfe7f0] bg-white">
        <div className="mx-auto flex w-[min(calc(100%_-_2rem),1440px)] flex-col gap-6 py-8 sm:w-[min(calc(100%_-_4rem),1440px)] sm:flex-row sm:items-center sm:justify-between">
          <Marca />
          <p className="m-0 text-xs leading-5 text-[#748196] sm:text-right">
            MVP de portfólio para organização e execução controlada de automações.
            <br />© {new Date().getFullYear()} FlowOps.
          </p>
        </div>
      </footer>
    </div>
  );
}

function PreviewProduto() {
  return (
    <div className="overflow-hidden rounded-xl border border-[#d7e1ed] bg-white shadow-[0_22px_55px_rgba(20,52,96,0.12)]" aria-label="Prévia da listagem de automações do FlowOps">
      <div className="flex min-h-12 items-center justify-between border-b border-[#e1e7ef] px-4">
        <span className="text-sm font-bold text-flowops-900">FlowOps</span>
        <span className="rounded-full bg-[#eef2f7] px-2.5 py-1 text-[10px] font-semibold text-[#536176]">Equipe Operações</span>
      </div>

      <div className="grid min-h-120 md:grid-cols-[150px_1fr]">
        <aside className="hidden border-r border-[#e1e7ef] bg-[#fbfcfe] p-3 md:flex md:flex-col" aria-label="Exemplo de navegação">
          <span className="flex min-h-9 items-center gap-2 rounded-md px-2 text-[10px] font-semibold text-[#657287]">
            <Workflow size={14} aria-hidden="true" /> Visão geral
          </span>
          <span className="flex min-h-9 items-center gap-2 rounded-md bg-flowops-50 px-2 text-[10px] font-bold text-flowops-700">
            <Workflow size={14} aria-hidden="true" /> Automações
          </span>
          <span className="mt-auto px-2 py-2 text-[10px] font-semibold text-[#657287]">Minha conta</span>
        </aside>

        <div className="min-w-0 p-4 sm:p-5">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <span className="text-[10px] font-semibold text-[#78869a]">Operação</span>
              <h2 className="m-0 mt-2 text-base">Automações</h2>
            </div>
            <span className="inline-flex min-h-8 items-center rounded-md bg-flowops-700 px-3 text-[10px] font-bold text-white mt-6">Nova automação</span>
          </div>

          <div className="mb-3 flex min-h-8 items-center rounded-md border border-[#dce4ee] px-3 text-[10px] text-[#8a96a7]">Buscar por nome</div>

          <div className="overflow-x-auto rounded-lg border border-[#dce4ee]">
            <table className="w-full min-w-125 border-collapse text-left text-[10px] lg:text-[11px]">
              <thead className="bg-[#f7f9fc] text-[#718096] uppercase">
                <tr>
                  <th className="px-3 py-2.5 font-bold">Automação</th>
                  <th className="px-2 py-2.5 font-bold">Status</th>
                  <th className="px-2 py-2.5 font-bold">Última execução</th>
                  <th className="px-2 py-2.5 font-bold">Duração</th>
                  <th className="px-3 py-2.5 font-bold">Ações</th>
                </tr>
              </thead>
              <tbody>
                {automacoesDemonstracao.map(([nome, status, execucao, duracao, podePausar]) => (
                  <tr className="border-t border-[#e5eaf1]" key={nome}>
                    <td className="max-w-40 px-3 py-3 font-semibold text-[#263247]">{nome}</td>
                    <td className="px-2 py-3">
                      <span className={`inline-flex rounded-full px-2 py-1 font-bold ${classesStatus[status]}`}>{status}</span>
                    </td>
                    <td className={`px-2 py-3 font-semibold ${classesExecucao[execucao]}`}>{execucao}</td>
                    <td className="px-2 py-3 text-[#5d6b7f]">{duracao}</td>
                    <td className="px-3 py-3">
                      <span className="flex items-center gap-2 text-flowops-700">
                        <History size={12} aria-hidden="true" />
                        <Play size={12} aria-hidden="true" />
                        {podePausar && <Pause size={12} aria-hidden="true" />}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
