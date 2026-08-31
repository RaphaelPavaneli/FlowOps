import { LogOut, ShieldCheck } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

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
    "whitespace-nowrap rounded-[9px] px-[13px] py-[9px] text-[12.5px] font-[650] no-underline transition-colors";
  const classesEstado = ativo
    ? "bg-flowops-50 text-flowops-700"
    : "text-[#667287] hover:bg-flowops-50 hover:text-flowops-700";

  return `${classesBase} ${classesEstado}`;
}

export function LayoutAutenticado() {
  const { usuario, sair } = useAutenticacao();

  if (!usuario) {
    return null;
  }

  const administrador = usuario.perfil_acesso === "administrador";

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="sticky top-0 z-20 border-b border-[#d7deea]/80 bg-white/90 backdrop-blur-2xl">
        <div className="grid min-h-[68px] w-full grid-cols-[auto_1fr] items-center px-4 min-[701px]:min-h-[76px] min-[701px]:px-6 min-[961px]:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] min-[961px]:px-[2%]">
          <Marca />

          <nav
            className="col-span-2 row-start-2 flex items-center justify-start gap-2 overflow-x-auto border-t border-[#edf1f6] pt-[7px] pb-2.5 min-[701px]:justify-center min-[961px]:col-span-1 min-[961px]:col-start-2 min-[961px]:row-start-1 min-[961px]:justify-self-center min-[961px]:overflow-visible min-[961px]:border-t-0 min-[961px]:py-0"
            aria-label="Navegação da aplicação"
          >
            <NavLink
              className={({ isActive }) => obterClasseNavegacao(isActive)}
              to="/app/dashboard"
            >
              Dashboard
            </NavLink>
            <NavLink
              className={({ isActive }) => obterClasseNavegacao(isActive)}
              to="/app/automacoes"
            >
              Automações
            </NavLink>
            {administrador && (
              <NavLink
                className={({ isActive }) => obterClasseNavegacao(isActive)}
                to="/app/administracao"
              >
                Administração
              </NavLink>
            )}
            <NavLink
              className={({ isActive }) => obterClasseNavegacao(isActive)}
              to="/app/minha-conta"
            >
              Minha conta
            </NavLink>
          </nav>

          <div className="col-start-2 row-start-1 flex items-center justify-self-end gap-2.5 min-[961px]:col-start-3">
            <span
              className="grid size-[35px] place-items-center rounded-[11px] bg-flowops-50 text-[11px] font-[750] text-flowops-700"
              aria-hidden="true"
            >
              {obterIniciais(usuario.nome)}
            </span>
            <span className="hidden max-w-[150px] flex-col gap-0.5 min-[701px]:flex">
              <strong className="overflow-hidden text-ellipsis whitespace-nowrap text-[11.5px] text-[#344055]">
                {usuario.nome}
              </strong>
              <small className="flex items-center gap-1 text-[9.5px] text-[#7c899c]">
                {administrador && <ShieldCheck size={12} aria-hidden="true" />}
                {administrador ? "Administrador" : "Usuário"}
              </small>
            </span>
            <button
              className="inline-flex size-[38px] min-h-[38px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-[#d7e1ef] bg-white/90 p-0 text-[12.5px] font-[650] text-[#536177] transition-colors hover:border-[#b9c9df] hover:bg-flowops-50 hover:text-flowops-700 min-[701px]:h-auto min-[701px]:w-auto min-[701px]:min-h-10 min-[701px]:px-[15px]"
              type="button"
              onClick={sair}
            >
              <LogOut size={17} aria-hidden="true" />
              <span className="hidden min-[701px]:inline">Sair</span>
            </button>
          </div>
        </div>
      </header>

      <Outlet />
    </div>
  );
}
