import { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  ArrowRight,
  Boxes,
  CheckCircle2,
  CircleGauge,
  Code2,
  Eye,
  Layers3,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { Marca } from "../components/Marca";

const beneficios = [
  {
    titulo: "Centralização",
    descricao:
      "Reunir processos, atividades e informações importantes em um único ambiente.",
    Icone: Layers3,
  },
  {
    titulo: "Visibilidade",
    descricao:
      "Facilitar o acompanhamento do que está acontecendo em toda a operação.",
    Icone: Eye,
  },
  {
    titulo: "Simplicidade",
    descricao:
      "Oferecer uma experiência clara, objetiva e agradável para quem utiliza.",
    Icone: Sparkles,
  },
];

const tecnologias = [
  "React e TypeScript",
  "FastAPI e Python",
  "SQLAlchemy e SQL Server",
  "JWT, Argon2id e testes",
];

export function PaginaInicial() {
  useEffect(() => {
    document.title = "FlowOps | Gestão empresarial com clareza";
  }, []);

  return (
    <div className="min-h-screen bg-white text-flowops-texto">
      <a
        className="fixed top-3 left-3 z-100 -translate-y-[160%] rounded-[9px] bg-flowops-700 px-3.5 py-2.5 text-white no-underline transition-transform duration-150 focus:translate-y-0"
        href="#conteudo-principal"
      >
        Ir para o conteúdo principal
      </a>

      <header className="sticky top-0 z-20 border-b border-slate-300/70 bg-white/90 backdrop-blur-2xl">
        <div className="mx-auto grid min-h-17 w-[min(calc(100%_-_2rem),1160px)] grid-cols-[1fr_auto] items-center sm:min-h-19 sm:w-[min(calc(100%_-_3rem),1160px)] lg:grid-cols-[1fr_auto_1fr]">
          <Marca />

          <nav className="hidden items-center gap-8.5 lg:flex" aria-label="Navegação principal">
            <a className="text-[13.5px] font-semibold text-flowops-cinza no-underline transition-colors duration-150 hover:text-flowops-700" href="#projeto">O projeto</a>
            <a className="text-[13.5px] font-semibold text-flowops-cinza no-underline transition-colors duration-150 hover:text-flowops-700" href="#recursos">Recursos</a>
            <a className="text-[13.5px] font-semibold text-flowops-cinza no-underline transition-colors duration-150 hover:text-flowops-700" href="#tecnologias">Tecnologias</a>
          </nav>

          <Link className="inline-flex min-h-10 items-center justify-center justify-self-end gap-2 rounded-xl border border-[#cfddf4] bg-white px-3.75 text-[13.5px] font-bold text-flowops-700 no-underline transition-[transform,border-color,background-color] duration-150 hover:-translate-y-px hover:border-[#aac5ef] hover:bg-flowops-50 sm:min-h-11.5 sm:px-5" to="/login">
            Entrar
            <ArrowRight size={17} aria-hidden="true" />
          </Link>
        </div>
      </header>

      <main id="conteudo-principal">
        <section className="relative flex min-h-auto items-center overflow-hidden bg-[radial-gradient(circle_at_83%_16%,rgba(191,219,254,0.5),transparent_30%),radial-gradient(circle_at_8%_86%,rgba(224,231,255,0.45),transparent_27%),linear-gradient(145deg,#fff_0%,#f9fbff_50%,#f7faff_100%)] py-[70px] sm:py-21 sm:pb-24 lg:min-h-[calc(100vh-76px)]">
          <div className="pointer-events-none absolute top-[8%] -right-[150px] h-[155px] w-[390px] rotate-[-8deg] rounded-l-[90px] border border-[rgba(105,144,224,0.16)]" aria-hidden="true" />
          <div className="pointer-events-none absolute bottom-[5%] -left-40 h-32.5 w-85 rotate-[8deg] rounded-r-[80px] border border-[rgba(105,144,224,0.16)]" aria-hidden="true" />

          <div className="relative z-2 mx-auto grid w-[min(calc(100%_-_2rem),1160px)] grid-cols-1 items-center gap-16 sm:w-[min(calc(100%_-_3rem),1160px)] lg:grid-cols-[minmax(0,1fr)_minmax(400px,0.88fr)] lg:gap-[clamp(3.5rem,8vw,7rem)]">
            <div className="mx-auto max-w-180 text-center lg:mx-0 lg:max-w-160 lg:text-left">
              <span className="mb-5.5 inline-flex items-center gap-1.75 rounded-full border border-[#d9e7fb] bg-flowops-50/86 px-3 py-1.75 text-[11px] font-bold tracking-[0.08em] text-[#315a9f] uppercase">
                <Sparkles size={15} aria-hidden="true" />
                Projeto pessoal full-stack
              </span>

              <h1 className="m-0 max-w-[690px] text-[clamp(2.375rem,11.5vw,3.25rem)] leading-[1.04] font-bold tracking-[-2px] text-flowops-texto sm:text-[clamp(2.625rem,5.2vw,4.125rem)] sm:tracking-[-2.8px]">
                Gestão empresarial com mais clareza e menos complexidade.
              </h1>

              <p className="mx-auto mt-6.25 max-w-150 text-[15.5px] leading-[1.7] text-flowops-cinza sm:text-[clamp(1rem,1.7vw,1.125rem)] lg:mx-0">
                Organize processos, acompanhe atividades e tenha uma visão
                centralizada da operação da sua empresa em um único lugar.
              </p>

              <div className="mt-8.5 flex flex-col items-center gap-3.5 sm:flex-row sm:flex-wrap sm:justify-center lg:justify-start">
                <a className="inline-flex min-h-11.5 w-full items-center justify-center gap-2 rounded-xl bg-linear-to-r from-flowops-700 to-flowops-500 px-5 text-[13.5px] font-bold text-white no-underline shadow-[0_12px_24px_rgba(37,99,235,0.2)] transition-[transform,box-shadow] duration-150 hover:-translate-y-px hover:shadow-[0_15px_30px_rgba(37,99,235,0.27)] sm:w-auto" href="#projeto">
                  Conhecer o projeto
                </a>
                <Link className="inline-flex min-h-11.5 w-full items-center justify-center gap-2 px-2 text-[13.5px] font-bold text-flowops-700 no-underline transition-transform duration-150 hover:-translate-y-px sm:w-auto" to="/login">
                  Acessar plataforma
                  <ArrowRight size={18} aria-hidden="true" />
                </Link>
              </div>

              <div className="mt-6.75 flex items-start justify-center gap-2 text-left text-[12.5px] text-[#6a7689] lg:items-center lg:justify-start">
                <ShieldCheck className="shrink-0 text-flowops-600" size={17} aria-hidden="true" />
                Construído com foco em segurança, clareza e evolução contínua.
              </div>
            </div>

            <div className="relative mx-auto w-full max-w-140 rounded-[18px] border border-white/95 bg-white/86 p-4.5 shadow-[0_32px_80px_rgba(30,64,175,0.13),0_8px_24px_rgba(15,23,42,0.06)] backdrop-blur-[15px] sm:rounded-[22px] sm:p-6 lg:max-w-none" aria-label="Prévia ilustrativa do FlowOps">
              <div className="flex items-start justify-between gap-2.5 sm:items-center">
                <div className="flex flex-col gap-1">
                  <span className="text-[11.5px] text-[#7a879b]">Visão geral</span>
                  <strong className="text-[17px]">Resumo da operação</strong>
                </div>
                <span className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full bg-emerald-50 px-2.25 py-1.5 text-[10.5px] font-semibold text-[#287355]">
                  <span className="size-1.5 rounded-full bg-[#34a476]" aria-hidden="true" /> Operação ativa
                </span>
              </div>

              <div className="my-5.5 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <article className="flex flex-col rounded-[14px] border border-[#e5ebf4] bg-[#fbfdff] p-4">
                  <span className="text-[11.5px] text-[#7a879b]">Processos ativos</span>
                  <strong className="my-1.5 mt-2.25 text-[28px] tracking-[-1px] text-flowops-900">08</strong>
                  <small className="flex items-center gap-1.25 text-[9.5px] text-[#5e6d82]"><CheckCircle2 className="text-flowops-600" size={13} /> Dentro do fluxo</small>
                </article>
                <article className="flex flex-col rounded-[14px] border border-[#e5ebf4] bg-[#fbfdff] p-4">
                  <span className="text-[11.5px] text-[#7a879b]">Atividades de hoje</span>
                  <strong className="my-1.5 mt-2.25 text-[28px] tracking-[-1px] text-flowops-900">12</strong>
                  <small className="flex items-center gap-1.25 text-[9.5px] text-[#5e6d82]"><CircleGauge className="text-flowops-600" size={13} /> Em acompanhamento</small>
                </article>
              </div>

              <div className="rounded-[14px] bg-flowops-50 p-4.25">
                <div className="mb-3.75 flex items-center justify-between text-[11.5px] font-semibold text-[#7a879b]">
                  <span>Fluxos recentes</span>
                  <span>Progresso</span>
                </div>
                <div className="flex items-center justify-start gap-2.5">
                  <span className="grid size-8.75 place-items-center rounded-[10px] bg-white text-flowops-700"><Boxes size={16} /></span>
                  <div className="flex flex-col gap-0.75">
                    <strong className="text-[11.5px]">Operação comercial</strong>
                    <span className="text-[11.5px] text-[#7a879b]">6 de 8 etapas concluídas</span>
                  </div>
                  <span className="ml-auto text-xs font-bold text-flowops-700">75%</span>
                </div>
                <div className="mt-3.25 h-1.25 overflow-hidden rounded-[10px] bg-[#dbe6f7]"><span className="block h-full w-3/4 rounded-[inherit] bg-linear-to-r from-flowops-700 to-[#5d8ff2]" /></div>
              </div>

              <span className="mt-2.75 block text-right text-[9.5px] text-[#909bae]">Dados meramente ilustrativos</span>
            </div>
          </div>
        </section>

        <section className="py-20.5 sm:py-28" id="projeto">
          <div className="mx-auto grid w-[min(calc(100%_-_2rem),1160px)] grid-cols-1 gap-7.5 sm:w-[min(calc(100%_-_3rem),1160px)] sm:gap-15 lg:grid-cols-[0.8fr_1.2fr] lg:gap-[clamp(3.75rem,10vw,8.75rem)]">
            <div>
              <span className="mb-3.5 block text-[11px] font-bold tracking-[0.11em] text-flowops-700 uppercase">O propósito</span>
              <h2 className="m-0 text-[31px] leading-[1.14] font-bold tracking-[-1px] text-flowops-texto sm:text-[clamp(1.875rem,4vw,2.6875rem)] sm:tracking-[-1.5px]">Por que o FlowOps foi criado?</h2>
            </div>

            <div className="grid gap-5">
              <p className="m-0 text-[15.5px] leading-[1.8] text-flowops-cinza">
                Muitas empresas ainda controlam suas operações usando planilhas
                separadas, mensagens, anotações e sistemas que não conversam
                entre si. Isso dificulta o acompanhamento e aumenta o risco de
                informações importantes se perderem.
              </p>
              <p className="m-0 text-[15.5px] leading-[1.8] text-flowops-cinza">
                O FlowOps nasceu como um projeto pessoal para explorar uma
                solução simples e centralizada de gerenciamento empresarial,
                aplicando boas práticas modernas de desenvolvimento full-stack.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-linear-to-b from-[#f8fbff] to-[#f5f9ff] py-20.5 sm:py-28" id="recursos">
          <div className="mx-auto w-[min(calc(100%_-_2rem),1160px)] sm:w-[min(calc(100%_-_3rem),1160px)]">
            <div className="mx-auto mb-13.75 max-w-162.5 text-center">
              <span className="mb-3.5 block text-[11px] font-bold tracking-[0.11em] text-flowops-700 uppercase">Objetivos do produto</span>
              <h2 className="m-0 text-[31px] leading-[1.14] font-bold tracking-[-1px] text-flowops-texto sm:text-[clamp(1.875rem,4vw,2.6875rem)] sm:tracking-[-1.5px]">Uma operação mais fácil de compreender</h2>
              <p className="mt-4.5 text-[15.5px] leading-[1.8] text-flowops-cinza">
                Três princípios orientam cada decisão de produto e mantêm a
                experiência organizada.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
              {beneficios.map(({ titulo, descricao, Icone }) => (
                <article className="rounded-[18px] border border-[#e4eaf3] bg-white/90 p-6.25 shadow-[0_12px_36px_rgba(30,64,175,0.05)] sm:p-7.5" key={titulo}>
                  <span className="grid size-11.25 place-items-center rounded-[13px] bg-flowops-50 text-flowops-700"><Icone size={22} /></span>
                  <h3 className="mt-5.5 mb-2.5 text-lg font-bold">{titulo}</h3>
                  <p className="m-0 text-[13.5px] leading-[1.7] text-flowops-cinza">{descricao}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20.5 sm:py-28" id="tecnologias">
          <div className="mx-auto grid w-[min(calc(100%_-_2rem),1160px)] grid-cols-1 items-center gap-9.5 rounded-[19px] border border-[#dce7f6] bg-[radial-gradient(circle_at_95%_0%,rgba(191,219,254,0.42),transparent_37%),#fbfdff] px-6 py-7.5 sm:w-[min(calc(100%_-_3rem),1160px)] sm:gap-9.5 sm:rounded-3xl sm:p-11 lg:grid-cols-[1.15fr_0.85fr] lg:gap-20 lg:p-15">
            <div>
              <span className="mb-6 grid size-11.25 place-items-center rounded-[13px] bg-flowops-50 text-flowops-700"><Code2 size={23} /></span>
              <span className="mb-3.5 block text-[11px] font-bold tracking-[0.11em] text-flowops-700 uppercase">Construção full-stack</span>
              <h2 className="m-0 text-[31px] leading-[1.14] font-bold tracking-[-1px] text-flowops-texto sm:text-[clamp(1.875rem,4vw,2.6875rem)] sm:tracking-[-1.5px]">Um projeto pessoal desenvolvido do início ao fim</h2>
              <p className="mt-5 text-[15.5px] leading-[1.8] text-flowops-cinza">
                O FlowOps representa uma jornada de evolução que conecta
                interface, regras de negócio, segurança, banco de dados e boas
                práticas de arquitetura.
              </p>
            </div>

            <ul className="m-0 grid list-none gap-3 p-0">
              {tecnologias.map((tecnologia) => (
                <li className="flex items-center gap-2.5 rounded-xl border border-[#e4eaf3] bg-white/90 px-4 py-3.5 text-[13px] font-semibold text-[#39475d]" key={tecnologia}>
                  <CheckCircle2 className="shrink-0 text-flowops-600" size={18} aria-hidden="true" />
                  {tecnologia}
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="pt-8 pb-20.5 sm:pb-28">
          <div className="mx-auto flex w-[min(calc(100%_-_2rem),1160px)] flex-col items-center text-center sm:w-[min(calc(100%_-_3rem),1160px)]">
            <span className="mb-5.5 grid size-11.25 place-items-center rounded-[13px] bg-flowops-50 text-flowops-700"><CircleGauge size={27} /></span>
            <h2 className="m-0 text-[31px] leading-[1.14] font-bold tracking-[-1px] text-flowops-texto sm:text-[clamp(1.875rem,4vw,2.6875rem)] sm:tracking-[-1.5px]">Pronto para conhecer o FlowOps?</h2>
            <p className="mt-3.75 text-[15.5px] leading-[1.8] text-flowops-cinza">Acesse a plataforma e acompanhe a evolução deste projeto.</p>
            <Link className="mt-7 inline-flex min-h-11.5 items-center justify-center gap-2 rounded-xl bg-linear-to-r from-flowops-700 to-flowops-500 px-5 text-[13.5px] font-bold text-white no-underline shadow-[0_12px_24px_rgba(37,99,235,0.2)] transition-[transform,box-shadow] duration-150 hover:-translate-y-px hover:shadow-[0_15px_30px_rgba(37,99,235,0.27)]" to="/login">
              Acessar plataforma
              <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-[#e8edf4] bg-[#fbfcfe]">
        <div className="mx-auto flex w-[min(calc(100%_-_2rem),1160px)] flex-col items-start gap-10 py-10.5 sm:w-[min(calc(100%_-_3rem),1160px)] sm:flex-row sm:items-center sm:justify-between">
          <div>
            <Marca />
            <p className="mt-2.5 mb-0 text-[11.5px] leading-[1.7] text-[#7a8799]">Gestão que flui com você.</p>
          </div>
          <p className="m-0 text-left text-[11.5px] leading-[1.7] text-[#7a8799] sm:text-right">
            Projeto pessoal desenvolvido para aprendizado e evolução full-stack.
            <br />© {new Date().getFullYear()} FlowOps.
          </p>
        </div>
      </footer>
    </div>
  );
}
