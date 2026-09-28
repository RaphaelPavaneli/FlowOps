import { useCallback, useEffect, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  RefreshCw,
  UserRound,
  Workflow,
} from "lucide-react";
import { Link, useLocation, useParams } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import { buscarExecucao, ErroExecucoes } from "../services/execucoes";
import type { Execucao, StatusExecucao } from "../types/execucoes";

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

interface CampoDetalheProps {
  titulo: string;
  valor: string;
  monoespacado?: boolean;
}

function CampoDetalhe({ titulo, valor, monoespacado }: CampoDetalheProps) {
  return (
    <div className="min-w-0 rounded-[12px] border border-[#e3e9f1] bg-[#fafbfd] p-4">
      <span className="mb-2 block text-[10px] font-bold tracking-[0.06em] text-[#7a8799] uppercase">
        {titulo}
      </span>
      <strong
        className={`block break-all text-[12px] leading-[1.6] text-[#344055] ${monoespacado ? "font-mono" : ""}`}
      >
        {valor}
      </strong>
    </div>
  );
}

export function PaginaDetalhesExecucao() {
  const { execucaoId } = useParams<{ execucaoId: string }>();
  const localizacao = useLocation();
  const { token, sair } = useAutenticacao();
  const nomeAutomacao = (localizacao.state as EstadoNavegacao | null)
    ?.automacaoNome;
  const [execucao, setExecucao] = useState<Execucao | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [atualizando, setAtualizando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    document.title = "Detalhes da execução | FlowOps";
  }, []);

  const carregarDetalhes = useCallback(
    async (carregamentoInicial = false) => {
      if (!token || !execucaoId) {
        setCarregando(false);
        setExecucao(null);
        setErro("Não foi possível identificar a execução selecionada.");
        return;
      }

      if (carregamentoInicial) {
        setCarregando(true);
      } else {
        setAtualizando(true);
      }
      setErro("");

      try {
        setExecucao(await buscarExecucao(token, execucaoId));
      } catch (falha) {
        if (falha instanceof ErroExecucoes && falha.status === 401) {
          sair();
          return;
        }

        setErro(
          falha instanceof ErroExecucoes
            ? falha.message
            : "Ocorreu um erro inesperado ao carregar os detalhes.",
        );
      } finally {
        setCarregando(false);
        setAtualizando(false);
      }
    },
    [token, execucaoId, sair],
  );

  useEffect(() => {
    void carregarDetalhes(true);
  }, [carregarDetalhes]);

  const automacaoId = execucao?.automacao_id;
  const voltarPara = automacaoId
    ? `/app/automacoes/${automacaoId}/execucoes`
    : "/app/automacoes";

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[#f7f9fc] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[980px] py-12 max-[700px]:w-[calc(100%_-_32px)] max-[700px]:py-9">
        <Link
          className="mb-6 inline-flex items-center gap-1.5 text-[12px] font-bold text-flowops-700 no-underline hover:text-flowops-800"
          to={voltarPara}
          state={{ automacaoNome: nomeAutomacao }}
        >
          <ArrowLeft size={16} aria-hidden="true" />
          Voltar para o histórico
        </Link>

        <section className="mb-7 flex items-end justify-between gap-5 max-[600px]:flex-col max-[600px]:items-start">
          <div>
            <span className="mb-2.5 block text-[10.5px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
              Operação
            </span>
            <h1 className="m-0 text-[clamp(30px,4vw,42px)] tracking-[-1.4px] text-flowops-texto">
              Detalhes da execução
            </h1>
            <p className="mt-2.5 mb-0 max-w-[650px] text-[13.5px] leading-[1.65] text-flowops-cinza">
              Consulte o estado atual, as referências e os horários registrados.
            </p>
          </div>

          {execucao && (
            <button
              className="inline-flex min-h-[42px] shrink-0 cursor-pointer items-center justify-center gap-2 rounded-[10px] border border-[#cfddf4] bg-white px-4 text-[12px] font-bold text-flowops-700 hover:bg-flowops-50 disabled:cursor-not-allowed disabled:opacity-55"
              type="button"
              disabled={atualizando}
              onClick={() => void carregarDetalhes()}
            >
              <RefreshCw
                className={atualizando ? "animate-spin" : ""}
                size={16}
                aria-hidden="true"
              />
              {atualizando ? "Atualizando..." : "Atualizar detalhes"}
            </button>
          )}
        </section>

        {carregando && (
          <section
            className="flex min-h-[320px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#e0e7f1] bg-white text-center text-flowops-cinza"
            aria-live="polite"
            aria-busy="true"
          >
            <span
              className="size-6 animate-spin rounded-full border-2 border-flowops-600/20 border-t-flowops-600"
              aria-hidden="true"
            />
            <p className="m-0 text-[13px]">Carregando detalhes...</p>
          </section>
        )}

        {!carregando && erro && !execucao && (
          <section
            className="flex min-h-[320px] flex-col items-center justify-center gap-4 rounded-[18px] border border-[#ecd8d6] bg-white p-8 text-center text-[#8f3029]"
            role="alert"
          >
            <AlertCircle size={28} aria-hidden="true" />
            <p className="m-0 max-w-[560px] text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-[#cfddf4] bg-white px-5 text-[13px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => void carregarDetalhes(true)}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && execucao && (
          <>
            {erro && (
              <div
                className="mb-5 flex items-center gap-2.5 rounded-[12px] border border-[#ecd8d6] bg-[#fff7f6] px-4 py-3 text-[12.5px] font-semibold text-[#8f3029]"
                role="alert"
              >
                <AlertCircle size={17} aria-hidden="true" />
                {erro}
              </div>
            )}

            <section className="rounded-[18px] border border-[#dfe7f1] bg-white p-6 shadow-[0_14px_38px_rgba(30,64,175,0.05)] max-[600px]:p-5">
              <div className="mb-6 flex flex-wrap items-center justify-between gap-4 border-b border-[#e8edf4] pb-5">
                <div className="flex items-center gap-3">
                  <span className="grid size-11 place-items-center rounded-[12px] bg-flowops-50 text-flowops-700">
                    <Workflow size={22} aria-hidden="true" />
                  </span>
                  <div>
                    <span className="block text-[10px] font-bold tracking-[0.06em] text-[#7a8799] uppercase">
                      Status atual
                    </span>
                    <span className={`mt-1 inline-flex w-fit rounded-full px-2.5 py-1.5 text-[10.5px] font-bold ${classesStatus[execucao.status]}`}>
                      {rotulosStatus[execucao.status]}
                    </span>
                  </div>
                </div>
                <span className="inline-flex items-center gap-1.5 text-[11px] text-[#788599]">
                  <RefreshCw size={13} aria-hidden="true" />
                  Atualizada em {formatarData(execucao.atualizada_em)}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 max-[650px]:grid-cols-1">
                <CampoDetalhe titulo="ID da execução" valor={execucao.id} monoespacado />
                <CampoDetalhe titulo="ID da automação" valor={execucao.automacao_id} monoespacado />
                <CampoDetalhe titulo="ID da equipe" valor={execucao.equipe_id} monoespacado />
                <CampoDetalhe titulo="ID do solicitante" valor={execucao.solicitada_por_usuario_id} monoespacado />
                <CampoDetalhe titulo="Solicitada em" valor={formatarData(execucao.criada_em)} />
                <CampoDetalhe titulo="Iniciada em" valor={formatarData(execucao.iniciada_em)} />
                <CampoDetalhe titulo="Finalizada em" valor={formatarData(execucao.finalizada_em)} />
                <CampoDetalhe titulo="Última atualização" valor={formatarData(execucao.atualizada_em)} />
              </div>

              {execucao.mensagem_erro && (
                <div className="mt-5 rounded-[12px] border border-[#ecd8d6] bg-[#fff7f6] p-4" role="alert">
                  <span className="mb-2 flex items-center gap-2 text-[11px] font-bold tracking-[0.05em] text-[#8f3029] uppercase">
                    <AlertCircle size={15} aria-hidden="true" />
                    Mensagem da falha
                  </span>
                  <p className="m-0 whitespace-pre-wrap break-words text-[12.5px] leading-[1.65] text-[#713a35]">
                    {execucao.mensagem_erro}
                  </p>
                </div>
              )}

              {!execucao.mensagem_erro && (
                <div className="mt-5 flex items-center gap-2 rounded-[12px] border border-[#e3e9f1] bg-[#fafbfd] px-4 py-3 text-[12px] text-[#69768a]">
                  <UserRound size={16} aria-hidden="true" />
                  Nenhuma mensagem de erro registrada para esta execução.
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </main>
  );
}
