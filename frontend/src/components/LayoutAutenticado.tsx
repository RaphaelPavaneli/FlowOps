import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  LogOut,
  Menu,
  ShieldCheck,
  UserRound,
  Workflow,
  X,
} from "lucide-react";
import { NavLink, Outlet, useLocation } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import { Marca } from "./Marca";

function obterIniciais(nome: string) {
  return nome
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((parte) => parte[0])
    .join("")
    .toUpperCase();
}

function obterClasseNavegacao(ativo: boolean) {
  const classesBase =
    "flex min-h-10 items-center gap-3 rounded-lg px-3 text-sm font-semibold no-underline transition-colors";
  const classesEstado = ativo
    ? "bg-white/10 text-white shadow-[inset_3px_0_0_#60a5fa]"
    : "text-[#c4d1e2] hover:bg-white/[0.07] hover:text-white";

  return `${classesBase} ${classesEstado}`;
}

interface NavegacaoLateralProps {
  administrador: boolean;
  aberta: boolean;
  nomeUsuario: string;
  perfilUsuario: string;
  aoFechar: () => void;
  aoSair: () => void;
}

function NavegacaoLateral({
  administrador,
  aberta,
  nomeUsuario,
  perfilUsuario,
  aoFechar,
  aoSair,
}: NavegacaoLateralProps) {
  return (
    <aside
      className={`fixed inset-y-0 left-0 z-50 flex w-[272px] flex-col border-r border-white/10 bg-[linear-gradient(180deg,var(--color-flowops-sidebar-top)_0%,var(--color-flowops-sidebar-middle)_52%,var(--color-flowops-sidebar-bottom)_100%)] transition-transform duration-200 lg:sticky lg:top-0 lg:z-20 lg:h-screen lg:w-[232px] lg:translate-x-0 ${
        aberta
          ? "visible translate-x-0"
          : "invisible -translate-x-full pointer-events-none lg:visible lg:pointer-events-auto"
      }`}
      id="navegacao-lateral"
      aria-label="Navegação principal"
    >
      <div className="flex min-h-16 items-center justify-between border-b border-white/10 px-4 lg:min-h-[72px] lg:px-5">
        <Marca clara />
        <button
          className="grid size-9 cursor-pointer place-items-center rounded-lg border-0 bg-transparent text-[#c4d1e2] hover:bg-white/10 hover:text-white lg:hidden"
          type="button"
          aria-label="Fechar navegação"
          onClick={aoFechar}
        >
          <X size={19} aria-hidden="true" />
        </button>
      </div>

      <div className="flex min-h-0 flex-1 flex-col px-3 py-5 lg:px-4">
        <span className="mb-2 px-3 text-[10px] font-bold tracking-[0.08em] text-[#7f9cc4] uppercase">
          Espaço de trabalho
        </span>

        <nav className="grid gap-1" aria-label="Áreas do FlowOps">
          <NavLink
            className={({ isActive }) => obterClasseNavegacao(isActive)}
            to="/app/dashboard"
          >
            <LayoutDashboard size={18} strokeWidth={1.8} aria-hidden="true" />
            Visão geral
          </NavLink>
          <NavLink
            className={({ isActive }) => obterClasseNavegacao(isActive)}
            to="/app/automacoes"
          >
            <Workflow size={18} strokeWidth={1.8} aria-hidden="true" />
            Automações
          </NavLink>
          {administrador && (
            <NavLink
              className={({ isActive }) => obterClasseNavegacao(isActive)}
              to="/app/administracao"
            >
              <ShieldCheck size={18} strokeWidth={1.8} aria-hidden="true" />
              Administração
            </NavLink>
          )}
        </nav>

        <div className="mt-auto border-t border-white/10 pt-4">
          <NavLink
            className={({ isActive }) => obterClasseNavegacao(isActive)}
            to="/app/minha-conta"
          >
            <UserRound size={18} strokeWidth={1.8} aria-hidden="true" />
            Minha conta
          </NavLink>

          <div className="mt-3 flex items-center gap-3 px-2 py-2">
            <span
              className="grid size-9 shrink-0 place-items-center rounded-full bg-white/10 text-[11px] font-bold text-white ring-1 ring-white/10"
              aria-hidden="true"
            >
              {obterIniciais(nomeUsuario)}
            </span>
            <span className="min-w-0 flex-1">
              <strong className="block truncate text-xs text-white">
                {nomeUsuario}
              </strong>
              <small className="mt-0.5 block text-[10px] text-[#93a8c5]">
                {perfilUsuario}
              </small>
            </span>
            <button
              className="grid size-9 shrink-0 cursor-pointer place-items-center rounded-lg border-0 bg-transparent text-[#a9bbd1] transition-colors hover:bg-white/10 hover:text-white"
              type="button"
              aria-label="Sair do FlowOps"
              title="Sair"
              onClick={aoSair}
            >
              <LogOut size={17} strokeWidth={1.8} aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}

export function LayoutAutenticado() {
  const { usuario, sair } = useAutenticacao();
  const localizacao = useLocation();
  const [navegacaoAberta, setNavegacaoAberta] = useState(false);

  useEffect(() => {
    setNavegacaoAberta(false);
  }, [localizacao.pathname]);

  useEffect(() => {
    if (!navegacaoAberta) {
      return;
    }

    const tratarTecla = (evento: KeyboardEvent) => {
      if (evento.key === "Escape") {
        setNavegacaoAberta(false);
      }
    };

    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", tratarTecla);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", tratarTecla);
    };
  }, [navegacaoAberta]);

  if (!usuario) {
    return null;
  }

  const administrador = usuario.perfil_acesso === "administrador";
  const perfilUsuario = administrador ? "Administrador" : "Usuário";

  return (
    <div className="min-h-screen bg-flowops-app lg:grid lg:grid-cols-[232px_minmax(0,1fr)]">
      <header className="sticky top-0 z-30 flex min-h-16 items-center justify-between border-b border-[#e2e7ee] bg-white px-4 lg:hidden">
        <button
          className="grid size-10 cursor-pointer place-items-center rounded-lg border border-[#dfe5ec] bg-white text-[#344055] hover:bg-[#f7f9fc]"
          type="button"
          aria-label="Abrir navegação"
          aria-controls="navegacao-lateral"
          aria-expanded={navegacaoAberta}
          onClick={() => setNavegacaoAberta(true)}
        >
          <Menu size={20} aria-hidden="true" />
        </button>
        <Marca />
        <span
          className="grid size-9 place-items-center rounded-full bg-[#eef2f6] text-[11px] font-bold text-[#344055]"
          aria-hidden="true"
        >
          {obterIniciais(usuario.nome)}
        </span>
      </header>

      {navegacaoAberta && (
        <button
          className="fixed inset-0 z-40 cursor-default border-0 bg-[#172033]/35 lg:hidden"
          type="button"
          aria-label="Fechar navegação"
          onClick={() => setNavegacaoAberta(false)}
        />
      )}

      <NavegacaoLateral
        administrador={administrador}
        aberta={navegacaoAberta}
        nomeUsuario={usuario.nome}
        perfilUsuario={perfilUsuario}
        aoFechar={() => setNavegacaoAberta(false)}
        aoSair={sair}
      />

      <div className="min-w-0 bg-flowops-app">
        <Outlet />
      </div>
    </div>
  );
}
