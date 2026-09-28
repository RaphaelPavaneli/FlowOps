import { useCallback, useEffect, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  CalendarClock,
  ChevronLeft,
  ChevronRight,
  Clock3,
  History,
  Search,
  RefreshCw,
} from "lucide-react";
import { Link, useLocation, useParams } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import { ErroExecucoes, listarExecucoes } from "../services/execucoes";
import type {
  ListaExecucoesResponse,
  StatusExecucao,
} from "../types/execucoes";

const ITENS_POR_PAGINA = 20;
const classesBotaoPaginacao =
  "inline-flex min-h-10 items-center justify-center gap-1.5 rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 text-[12px] font-bold text-[#526077] transition-colors enabled:cursor-pointer enabled:hover:border-[#adc4e8] enabled:hover:bg-flowops-50 enabled:hover:text-flowops-700 disabled:cursor-not-allowed disabled:opacity-45";

const rotulosStatus: Record<StatusExecucao, string> = {
  pendente: "Pendente",
  processando: "Processando",
  concluida: "Concluída",
  falhou: "Falhou",
};

const classesStatus: Record<StatusExecucao, string> = {
  pendente: "bg-[#fff8e8] text-[#8a6724]",
  processando: "bg-[#eff6ff] text-[#275ea8]",
  concluida: "bg-[#ecfdf3] text-[#237a45]",
  falhou: "bg-[#fff1f0] text-[#9f312b]",
};

function formatarData(data: string | null) {
  if (!data) {
    return "Ainda não registrada";
  }

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(data));
}

interface EstadoNavegacao {
  automacaoNome?: string;
}

export function PaginaHistoricoExecucoes() {
  const { automacaoId } = useParams<{ automacaoId: string }>();
  const localizacao = useLocation();
  const { token, sair } = useAutenticacao();
  const nomeAutomacao = (localizacao.state as EstadoNavegacao | null)
    ?.automacaoNome;
  const [pagina, setPagina] = useState(1);
  const [resultado, setResultado] =
    useState<ListaExecucoesResponse | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    document.title = "Histórico de execuções | FlowOps";
  }, []);

  const carregarHistorico = useCallback(async () => {
    if (!token || !automacaoId) {
      setCarregando(false);
      setResultado(null);
      setErro("Não foi possível identificar a automação selecionada.");
      return;
    }

    setCarregando(true);
    setErro("");

    try {
      setResultado(
        await listarExecucoes(
          token,
          automacaoId,
          pagina,
          ITENS_POR_PAGINA,
        ),
      );
    } catch (falha) {
      if (falha instanceof ErroExecucoes && falha.status === 401) {
        sair();
        return;
      }

      setErro(
        falha instanceof ErroExecucoes
          ? falha.message
          : "Ocorreu um erro inesperado ao carregar o histórico.",
      );
    } finally {
      setCarregando(false);
    }
  }, [token, automacaoId, pagina, sair]);

  useEffect(() => {
    void carregarHistorico();
  }, [carregarHistorico]);

  const totalPaginas = Math.max(resultado?.total_paginas ?? 1, 1);

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[#f7f9fc] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] py-12 max-[700px]:w-[calc(100%_-_32px)] max-[700px]:py-9">
        <Link
          className="mb-6 inline-flex items-center gap-1.5 text-[12px] font-bold text-flowops-700 no-underline hover:text-flowops-800"
          to="/app/automacoes"
        >
          <ArrowLeft size={16} aria-hidden="true" />
          Voltar para automações
        </Link>

        <section className="mb-7">
          <span className="mb-2.5 block text-[10.5px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
            Operação
          </span>
          <h1 className="m-0 text-[clamp(30px,4vw,42px)] tracking-[-1.4px] text-flowops-texto">
            Histórico de execuções
          </h1>
          <p className="mt-2.5 mb-0 max-w-[760px] text-[13.5px] leading-[1.65] text-flowops-cinza">
            {nomeAutomacao
              ? `Acompanhe as execuções de “${nomeAutomacao}”.`
              : "Acompanhe as execuções da automação selecionada."}
          </p>
        </section>

        {carregando && (
          <section
            className="flex min-h-[300px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#e0e7f1] bg-white text-center text-flowops-cinza"
            aria-live="polite"
            aria-busy="true"
          >
            <span
              className="size-6 animate-spin rounded-full border-2 border-flowops-600/20 border-t-flowops-600"
              aria-hidden="true"
            />
            <p className="m-0 text-[13px]">Carregando histórico...</p>
          </section>
        )}

        {!carregando && erro && (
          <section
            className="flex min-h-[300px] flex-col items-center justify-center gap-4 rounded-[18px] border border-[#ecd8d6] bg-white p-8 text-center text-[#8f3029]"
            role="alert"
          >
            <AlertCircle size={28} aria-hidden="true" />
            <p className="m-0 max-w-[560px] text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-[#cfddf4] bg-white px-5 text-[13px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => void carregarHistorico()}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resultado?.execucoes.length === 0 && (
          <section className="flex min-h-[300px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#e0e7f1] bg-white p-8 text-center">
            <span className="grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700">
              <History size={25} aria-hidden="true" />
            </span>
            <h2 className="m-0 text-[17px] text-flowops-texto">
              Nenhuma execução registrada
            </h2>
            <p className="m-0 max-w-[500px] text-[13px] leading-[1.6] text-flowops-cinza">
              Quando uma execução for solicitada, ela aparecerá neste histórico.
            </p>
          </section>
        )}

        {!carregando && !erro && resultado && resultado.execucoes.length > 0 && (
          <>
            <section
              className="overflow-hidden rounded-[18px] border border-[#dfe7f1] bg-white shadow-[0_14px_38px_rgba(30,64,175,0.05)]"
              aria-label="Histórico de execuções"
            >
              <div className="hidden grid-cols-[minmax(170px,1fr)_minmax(105px,0.42fr)_minmax(145px,0.62fr)_minmax(145px,0.62fr)_minmax(105px,0.4fr)] gap-5 border-b border-[#e7ecf3] bg-[#f8fafd] px-6 py-3.5 text-[10px] font-bold tracking-[0.07em] text-[#7a8799] uppercase min-[701px]:grid">
                <span>Execução</span>
                <span>Status</span>
                <span>Solicitada em</span>
                <span>Finalizada em</span>
                <span>Ações</span>
              </div>

              <ul className="m-0 list-none p-0">
                {resultado.execucoes.map((execucao) => (
                  <li
                    className="grid gap-4 border-b border-[#edf1f6] px-5 py-5 last:border-b-0 min-[701px]:grid-cols-[minmax(170px,1fr)_minmax(105px,0.42fr)_minmax(145px,0.62fr)_minmax(145px,0.62fr)_minmax(105px,0.4fr)] min-[701px]:items-center min-[701px]:gap-5 min-[701px]:px-6"
                    key={execucao.id}
                  >
                    <div className="min-w-0">
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Execução
                      </span>
                      <strong className="block truncate font-mono text-[11.5px] text-[#344055]" title={execucao.id}>
                        {execucao.id}
                      </strong>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Status
                      </span>
                      <span className={`inline-flex w-fit rounded-full px-2.5 py-1.5 text-[10.5px] font-bold ${classesStatus[execucao.status]}`}>
                        {rotulosStatus[execucao.status]}
                      </span>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Solicitada em
                      </span>
                      <span className="inline-flex items-center gap-1.5 text-[11.5px] text-[#667388]">
                        <CalendarClock size={14} aria-hidden="true" />
                        {formatarData(execucao.criada_em)}
                      </span>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Finalizada em
                      </span>
                      <span className="inline-flex items-center gap-1.5 text-[11.5px] text-[#667388]">
                        <Clock3 size={14} aria-hidden="true" />
                        {formatarData(execucao.finalizada_em)}
                      </span>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Ações
                      </span>
                      <Link
                        className="inline-flex min-h-9 items-center justify-center gap-1.5 rounded-[9px] border border-[#cfddf4] bg-white px-3 text-[11px] font-bold text-flowops-700 no-underline transition-colors hover:bg-flowops-50"
                        to={`/app/execucoes/${execucao.id}`}
                        state={{ automacaoNome: nomeAutomacao }}
                      >
                        <Search size={14} aria-hidden="true" />
                        Detalhes
                      </Link>
                    </div>
                  </li>
                ))}
              </ul>
            </section>

            <nav
              className="mt-5 flex items-center justify-between gap-4 rounded-[14px] border border-[#e1e8f1] bg-white px-4 py-3 max-[520px]:flex-wrap max-[520px]:justify-center"
              aria-label="Paginação do histórico de execuções"
            >
              <button
                className={classesBotaoPaginacao}
                type="button"
                disabled={pagina <= 1}
                onClick={() => setPagina((atual) => Math.max(1, atual - 1))}
              >
                <ChevronLeft size={16} aria-hidden="true" />
                Anterior
              </button>

              <span className="text-[11.5px] font-semibold text-[#69768a]">
                Página {resultado.pagina} de {totalPaginas} · {resultado.total}{" "}
                {resultado.total === 1 ? "execução" : "execuções"}
              </span>

              <button
                className={classesBotaoPaginacao}
                type="button"
                disabled={pagina >= totalPaginas}
                onClick={() => setPagina((atual) => atual + 1)}
              >
                Próxima
                <ChevronRight size={16} aria-hidden="true" />
              </button>
            </nav>
          </>
        )}
      </div>
    </main>
  );
}
