import { useCallback, useEffect, useState } from "react";
import {
  ArrowRight,
  CircleGauge,
  RefreshCw,
  ShieldCheck,
  UserCheck,
  UserRoundCog,
  UsersRound,
  UserX,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import {
  ErroDashboard,
  obterResumoDashboard,
} from "../services/dashboard";
import type { ResumoDashboard } from "../types/dashboard";

export function PaginaDashboard() {
  const { token, usuario, sair } = useAutenticacao();
  const navegar = useNavigate();
  const [resumo, setResumo] = useState<ResumoDashboard | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    document.title = "Dashboard | FlowOps";
  }, []);

  const carregarResumo = useCallback(async () => {
    if (!token) {
      return;
    }

    setCarregando(true);
    setErro("");

    try {
      setResumo(await obterResumoDashboard(token));
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
      ]
    : [];

  return (
    <main className="pagina-dashboard">
      <div className="container conteudo-dashboard">
        <section className="cabecalho-dashboard">
          <div>
            <span className="sobretitulo">Visão geral</span>
            <h1>Bem-vindo, {usuario?.nome}</h1>
            <p>Acompanhe as principais informações administrativas da operação.</p>
          </div>
          <span className="data-dashboard">
            <CircleGauge size={18} aria-hidden="true" />
            Dados atualizados pelo FlowOps
          </span>
        </section>

        {carregando && (
          <section className="estado-dashboard" aria-live="polite" aria-busy="true">
            <span className="indicador-carregamento indicador-carregamento-azul" />
            <p>Carregando informações do dashboard...</p>
          </section>
        )}

        {!carregando && erro && (
          <section className="estado-dashboard estado-dashboard-erro" role="alert">
            <p>{erro}</p>
            <button className="botao botao-secundario" type="button" onClick={carregarResumo}>
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resumo && (
          <>
            <section className="grade-metricas" aria-label="Resumo de usuários">
              {metricas.map(({ titulo, valor, Icone }) => (
                <article className="cartao-metrica" key={titulo}>
                  <span className="icone-metrica"><Icone size={21} /></span>
                  <span>{titulo}</span>
                  <strong>{valor}</strong>
                </article>
              ))}
            </section>

            <section className="cartao-acesso-administracao">
              <div className="icone-administracao-dashboard" aria-hidden="true">
                <UserRoundCog size={27} />
              </div>
              <div>
                <span>Área exclusiva</span>
                <h2>Administração</h2>
                <p>Gerencie configurações e os futuros módulos administrativos da plataforma.</p>
              </div>
              <Link className="botao botao-primario" to="/app/administracao">
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
