import { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import type { PerfilAcesso } from "../types/autenticacao";

interface PropriedadesRotaProtegida {
  children: ReactNode;
  perfisPermitidos?: PerfilAcesso[];
}

export function RotaProtegida({
  children,
  perfisPermitidos,
}: PropriedadesRotaProtegida) {
  const { autenticado, usuario } = useAutenticacao();
  const localizacao = useLocation();

  if (!autenticado) {
    return (
      <Navigate
        to="/login"
        replace
        state={{ origem: localizacao.pathname }}
      />
    );
  }

  if (
    perfisPermitidos &&
    usuario &&
    !perfisPermitidos.includes(usuario.perfil_acesso)
  ) {
    return <Navigate to="/app/acesso-negado" replace />;
  }

  return children;
}
