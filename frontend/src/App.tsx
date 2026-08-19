import { Navigate, Route, Routes } from "react-router-dom";

import { RotaProtegida } from "./components/RotaProtegida";
import { LayoutAutenticado } from "./components/LayoutAutenticado";
import { useAutenticacao } from "./contexts/ContextoAutenticacao";
import { PaginaAcessoNegado } from "./pages/PaginaAcessoNegado";
import { PaginaAdministracao } from "./pages/PaginaAdministracao";
import { PaginaAreaAutenticada } from "./pages/PaginaAreaAutenticada";
import { PaginaDashboard } from "./pages/PaginaDashboard";
import { PaginaInicial } from "./pages/PaginaInicial";
import { PaginaLogin } from "./pages/PaginaLogin";
import { PaginaNaoEncontrada } from "./pages/PaginaNaoEncontrada";

function App() {
  const { autenticado, carregandoSessao, usuario } = useAutenticacao();

  if (carregandoSessao) {
    return (
      <main className="pagina-carregando-sessao" aria-busy="true">
        <span className="indicador-carregamento indicador-carregamento-azul" />
        <p>Validando sua sessão...</p>
      </main>
    );
  }

  return (
    <Routes>
      <Route path="/" element={<PaginaInicial />} />
      <Route
        path="/login"
        element={
          autenticado ? (
            <Navigate
              to={usuario?.perfil_acesso === "administrador" ? "/app/dashboard" : "/app"}
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
        <Route index element={<PaginaAreaAutenticada />} />
        <Route
          path="dashboard"
          element={
            <RotaProtegida perfisPermitidos={["administrador"]}>
              <PaginaDashboard />
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
        <Route path="acesso-negado" element={<PaginaAcessoNegado />} />
      </Route>
      <Route path="*" element={<PaginaNaoEncontrada />} />
    </Routes>
  );
}

export default App;
