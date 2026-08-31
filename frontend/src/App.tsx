import { Navigate, Route, Routes } from "react-router-dom";

import { RotaProtegida } from "./components/RotaProtegida";
import { LayoutAutenticado } from "./components/LayoutAutenticado";
import { useAutenticacao } from "./contexts/ContextoAutenticacao";
import { PaginaAcessoNegado } from "./pages/PaginaAcessoNegado";
import { PaginaAdministracao } from "./pages/PaginaAdministracao";
import { PaginaAutomacoes } from "./pages/PaginaAutomacoes";
import { PaginaCadastro } from "./pages/PaginaCadastro";
import { PaginaDashboardAdministrativo } from "./pages/PaginaDashboardAdministrativo";
import { PaginaDashboardOperacional } from "./pages/PaginaDashboardOperacional";
import { PaginaGestaoEquipes } from "./pages/PaginaGestaoEquipes";
import { PaginaGestaoUsuarios } from "./pages/PaginaGestaoUsuarios";
import { PaginaInicial } from "./pages/PaginaInicial";
import { PaginaLogin } from "./pages/PaginaLogin";
import { PaginaMinhaConta } from "./pages/PaginaMinhaConta";
import { PaginaNaoEncontrada } from "./pages/PaginaNaoEncontrada";

function App() {
  const { autenticado, carregandoSessao } = useAutenticacao();

  if (carregandoSessao) {
    return (
      <main
        className="flex min-h-screen flex-col items-center justify-center gap-3.5 bg-[radial-gradient(circle_at_50%_38%,rgba(191,219,254,0.45),transparent_24%),#f8fafc] text-[13px] text-flowops-cinza"
        aria-busy="true"
      >
        <span
          className="size-6 animate-spin rounded-full border-2 border-flowops-600/20 border-t-flowops-600"
          aria-hidden="true"
        />
        <p className="m-0">Validando sua sessão...</p>
      </main>
    );
  }

  return (
    <Routes>
      <Route path="/" element={<PaginaInicial />} />
      <Route
        path="/cadastro"
        element={
          autenticado ? (
            <Navigate to="/app/dashboard" replace />
          ) : (
            <PaginaCadastro />
          )
        }
      />
      <Route
        path="/login"
        element={
          autenticado ? (
            <Navigate
              to="/app/dashboard"
              replace
            />
          ) : (
            <PaginaLogin />
          )
        }
      />
      <Route
        path="/app"
        element={
          <RotaProtegida>
            <LayoutAutenticado />
          </RotaProtegida>
        }
      >
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<PaginaDashboardOperacional />} />
        <Route path="automacoes" element={<PaginaAutomacoes />} />
        <Route path="minha-conta" element={<PaginaMinhaConta />} />
        <Route
          path="administracao/dashboard"
          element={
            <RotaProtegida perfisPermitidos={["administrador"]}>
              <PaginaDashboardAdministrativo />
            </RotaProtegida>
          }
        />
        <Route
          path="administracao"
          element={
            <RotaProtegida perfisPermitidos={["administrador"]}>
              <PaginaAdministracao />
            </RotaProtegida>
          }
        />
        <Route
          path="administracao/usuarios"
          element={
            <RotaProtegida perfisPermitidos={["administrador"]}>
              <PaginaGestaoUsuarios />
            </RotaProtegida>
          }
        />
        <Route
          path="administracao/equipes"
          element={
            <RotaProtegida perfisPermitidos={["administrador"]}>
              <PaginaGestaoEquipes />
            </RotaProtegida>
          }
        />
        <Route path="acesso-negado" element={<PaginaAcessoNegado />} />
      </Route>
      <Route path="*" element={<PaginaNaoEncontrada />} />
    </Routes>
  );
}

export default App;
