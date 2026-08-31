import { FormEvent, useCallback, useEffect, useState } from "react";
import {
  CalendarDays,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Clock3,
  FilePlus2,
  LoaderCircle,
  Plus,
  RefreshCw,
  Workflow,
  X,
} from "lucide-react";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import {
  criarAutomacao,
  ErroAutomacoes,
  listarAutomacoes,
} from "../services/automacoes";
import type {
  ListaAutomacoesResponse,
  StatusAutomacao,
} from "../types/automacoes";

const ITENS_POR_PAGINA = 20;
const classesBotaoPaginacao =
  "inline-flex min-h-10 items-center justify-center gap-1.5 rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 text-[12px] font-bold text-[#526077] transition-colors enabled:cursor-pointer enabled:hover:border-[#adc4e8] enabled:hover:bg-flowops-50 enabled:hover:text-flowops-700 disabled:cursor-not-allowed disabled:opacity-45";

const rotulosStatus: Record<StatusAutomacao, string> = {
  rascunho: "Rascunho",
  ativa: "Ativa",
  pausada: "Pausada",
};

const classesStatus: Record<StatusAutomacao, string> = {
  rascunho: "bg-[#f2f5f9] text-[#657287]",
  ativa: "bg-[#ecfdf3] text-[#237a45]",
  pausada: "bg-[#fff8e8] text-[#8a6724]",
};

function formatarData(data: string) {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(data));
}

export function PaginaAutomacoes() {
  const { token, usuario, sair } = useAutenticacao();
  const [pagina, setPagina] = useState(1);
  const [resultado, setResultado] = useState<ListaAutomacoesResponse | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [formularioAberto, setFormularioAberto] = useState(false);
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [salvando, setSalvando] = useState(false);
  const [mensagemAcao, setMensagemAcao] = useState<{
    tipo: "sucesso" | "erro";
    texto: string;
  } | null>(null);

  useEffect(() => {
    document.title = "Automações | FlowOps";
  }, []);

  const carregarAutomacoes = useCallback(async () => {
    if (!token || !usuario?.equipe_id) {
      setCarregando(false);
      setResultado(null);
      setErro("");
      return;
    }

    setCarregando(true);
    setErro("");

    try {
      setResultado(
        await listarAutomacoes(token, pagina, ITENS_POR_PAGINA),
      );
    } catch (falha) {
      if (falha instanceof ErroAutomacoes && falha.status === 401) {
        sair();
        return;
      }

      setErro(
        falha instanceof ErroAutomacoes
          ? falha.message
          : "Ocorreu um erro inesperado ao carregar as automações.",
      );
    } finally {
      setCarregando(false);
    }
  }, [token, usuario?.equipe_id, pagina, sair]);

  useEffect(() => {
    void carregarAutomacoes();
  }, [carregarAutomacoes]);

  function fecharFormulario() {
    if (salvando) {
      return;
    }
    setFormularioAberto(false);
    setNome("");
    setDescricao("");
    setMensagemAcao(null);
  }

  async function enviarFormulario(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();

    if (!token || !usuario?.equipe_id || salvando) {
      return;
    }

    const nomeLimpo = nome.trim().replace(/\s+/g, " ");
    if (nomeLimpo.length < 2) {
      setMensagemAcao({
        tipo: "erro",
        texto: "Informe um nome com pelo menos 2 caracteres.",
      });
      return;
    }

    setSalvando(true);
    setMensagemAcao(null);

    try {
      await criarAutomacao(token, {
        nome: nomeLimpo,
        descricao: descricao.trim() || null,
      });
      setNome("");
      setDescricao("");
      setFormularioAberto(false);
      setMensagemAcao({
        tipo: "sucesso",
        texto: "Automação criada com sucesso.",
      });

      if (pagina === 1) {
        await carregarAutomacoes();
      } else {
        setPagina(1);
      }
    } catch (falha) {
      if (falha instanceof ErroAutomacoes && falha.status === 401) {
        sair();
        return;
      }

      setMensagemAcao({
        tipo: "erro",
        texto:
          falha instanceof ErroAutomacoes
            ? falha.message
            : "Ocorreu um erro inesperado ao criar a automação.",
      });
    } finally {
      setSalvando(false);
    }
  }

  const totalPaginas = Math.max(resultado?.total_paginas ?? 1, 1);

  if (usuario?.equipe_id === null) {
    return (
      <main className="min-h-[calc(100vh-77px)] bg-[#f7f9fc] max-[700px]:min-h-[calc(100vh-116px)]">
        <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] py-12 max-[700px]:w-[calc(100%_-_32px)] max-[700px]:py-9">
          <section className="mb-7">
            <span className="mb-2.5 block text-[10.5px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
              Operação
            </span>
            <h1 className="m-0 text-[clamp(30px,4vw,42px)] tracking-[-1.4px] text-flowops-texto">
              Automações
            </h1>
            <p className="mt-2.5 mb-0 max-w-[630px] text-[13.5px] leading-[1.65] text-flowops-cinza">
              As automações ficam disponíveis depois que sua conta entra em uma
              equipe.
            </p>
          </section>

          <section
            className="flex min-h-[320px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#eadfbf] bg-white p-8 text-center shadow-[0_14px_38px_rgba(30,64,175,0.04)]"
            aria-labelledby="titulo-automacoes-sem-equipe"
          >
            <span
              className="grid size-12 place-items-center rounded-[14px] bg-[#fff5d8] text-[#8a6724]"
              aria-hidden="true"
            >
              <Clock3 size={24} />
            </span>
            <h2
              className="m-0 text-[18px] text-flowops-texto"
              id="titulo-automacoes-sem-equipe"
            >
              Aguardando associação a uma equipe
            </h2>
            <p className="m-0 max-w-[540px] text-[13px] leading-[1.65] text-flowops-cinza">
              Sua conta está ativa, mas um administrador precisa vinculá-la a
              uma equipe antes que as automações compartilhadas sejam liberadas.
            </p>
            <button
              className="mt-2 inline-flex min-h-[42px] cursor-pointer items-center justify-center gap-2 rounded-[10px] border border-[#cfddf4] bg-white px-4 text-[12px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => window.location.reload()}
            >
              <RefreshCw size={16} aria-hidden="true" />
              Atualizar situação
            </button>
          </section>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[#f7f9fc] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] py-12 max-[700px]:w-[calc(100%_-_32px)] max-[700px]:py-9">
        <section className="mb-7 flex items-end justify-between gap-6 max-[700px]:flex-col max-[700px]:items-start">
          <div>
            <span className="mb-2.5 block text-[10.5px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
              Operação
            </span>
            <h1 className="m-0 text-[clamp(30px,4vw,42px)] tracking-[-1.4px] text-flowops-texto">
              Automações
            </h1>
            <p className="mt-2.5 mb-0 max-w-[630px] text-[13.5px] leading-[1.65] text-flowops-cinza">
              Cadastre e acompanhe as automações compartilhadas com a sua equipe.
            </p>
          </div>

          <button
            className="inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-flowops-700 bg-flowops-700 px-5 text-[12.5px] font-bold text-white transition-colors hover:bg-flowops-800 disabled:cursor-not-allowed disabled:opacity-55"
            type="button"
            disabled={salvando}
            onClick={() => {
              setFormularioAberto(true);
              setMensagemAcao(null);
            }}
          >
            <Plus size={17} aria-hidden="true" />
            Nova automação
          </button>
        </section>

        {formularioAberto && (
          <section className="mb-6 rounded-[18px] border border-[#cfddf4] bg-white p-6 shadow-[0_14px_38px_rgba(30,64,175,0.06)] max-[600px]:p-5">
            <div className="mb-5 flex items-start justify-between gap-4">
              <div>
                <h2 className="m-0 text-[18px] text-flowops-texto">
                  Criar automação
                </h2>
                <p className="mt-1.5 mb-0 text-[12.5px] text-flowops-cinza">
                  A equipe, o criador e o status inicial serão definidos pelo sistema.
                </p>
              </div>
              <button
                className="grid size-9 shrink-0 cursor-pointer place-items-center rounded-[9px] border border-[#dde5ef] bg-white text-[#69768a] hover:bg-[#f5f7fa]"
                type="button"
                aria-label="Fechar formulário"
                disabled={salvando}
                onClick={fecharFormulario}
              >
                <X size={17} aria-hidden="true" />
              </button>
            </div>

            <form className="grid gap-4" onSubmit={enviarFormulario}>
              <label className="grid gap-1.5">
                <span className="text-[11.5px] font-bold text-[#455268]">Nome</span>
                <input
                  className="min-h-[44px] rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 text-[13px] text-flowops-texto outline-none transition-colors focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:bg-[#f4f6f8]"
                  type="text"
                  value={nome}
                  minLength={2}
                  maxLength={120}
                  required
                  autoFocus
                  disabled={salvando}
                  placeholder="Ex.: Importação diária de pedidos"
                  onChange={(evento) => setNome(evento.target.value)}
                />
              </label>

              <label className="grid gap-1.5">
                <span className="text-[11.5px] font-bold text-[#455268]">
                  Descrição <span className="font-normal text-[#8995a5]">(opcional)</span>
                </span>
                <textarea
                  className="min-h-[100px] resize-y rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 py-3 text-[13px] leading-[1.55] text-flowops-texto outline-none transition-colors focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:bg-[#f4f6f8]"
                  value={descricao}
                  maxLength={500}
                  disabled={salvando}
                  placeholder="Descreva brevemente o objetivo desta automação."
                  onChange={(evento) => setDescricao(evento.target.value)}
                />
                <small className="justify-self-end text-[10px] text-[#8995a5]">
                  {descricao.length}/500
                </small>
              </label>

              {mensagemAcao?.tipo === "erro" && (
                <p
                  className="m-0 rounded-[10px] border border-[#ecd8d6] bg-[#fff7f6] px-3.5 py-3 text-[12px] font-semibold text-[#8f3029]"
                  role="alert"
                >
                  {mensagemAcao.texto}
                </p>
              )}

              <div className="flex justify-end gap-2.5 max-[480px]:flex-col-reverse">
                <button
                  className="inline-flex min-h-[42px] cursor-pointer items-center justify-center rounded-[10px] border border-[#d6e0ee] bg-white px-4 text-[12px] font-bold text-[#5e6c80] hover:bg-[#f6f8fa] disabled:cursor-not-allowed disabled:opacity-55"
                  type="button"
                  disabled={salvando}
                  onClick={fecharFormulario}
                >
                  Cancelar
                </button>
                <button
                  className="inline-flex min-h-[42px] cursor-pointer items-center justify-center gap-2 rounded-[10px] border border-flowops-700 bg-flowops-700 px-5 text-[12px] font-bold text-white hover:bg-flowops-800 disabled:cursor-not-allowed disabled:opacity-55"
                  type="submit"
                  disabled={salvando}
                >
                  {salvando ? (
                    <LoaderCircle className="animate-spin" size={16} aria-hidden="true" />
                  ) : (
                    <FilePlus2 size={16} aria-hidden="true" />
                  )}
                  {salvando ? "Criando..." : "Criar automação"}
                </button>
              </div>
            </form>
          </section>
        )}

        {mensagemAcao?.tipo === "sucesso" && (
          <div
            className="mb-5 flex items-center gap-2.5 rounded-[12px] border border-[#ccebd7] bg-[#f0fdf4] px-4 py-3 text-[12.5px] font-semibold text-[#237a45]"
            role="status"
          >
            <CheckCircle2 size={17} aria-hidden="true" />
            {mensagemAcao.texto}
          </div>
        )}

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
            <p className="m-0 text-[13px]">Carregando automações...</p>
          </section>
        )}

        {!carregando && erro && (
          <section
            className="flex min-h-[300px] flex-col items-center justify-center gap-4 rounded-[18px] border border-[#ecd8d6] bg-white p-8 text-center text-[#8f3029]"
            role="alert"
          >
            <p className="m-0 max-w-[560px] text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-[#cfddf4] bg-white px-5 text-[13px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => void carregarAutomacoes()}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resultado?.automacoes.length === 0 && (
          <section className="flex min-h-[300px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#e0e7f1] bg-white p-8 text-center">
            <span className="grid size-12 place-items-center rounded-[14px] bg-flowops-50 text-flowops-700">
              <Workflow size={25} aria-hidden="true" />
            </span>
            <h2 className="m-0 text-[17px] text-flowops-texto">
              Nenhuma automação cadastrada
            </h2>
            <p className="m-0 max-w-[480px] text-[13px] leading-[1.6] text-flowops-cinza">
              Crie a primeira automação para que ela fique disponível para a sua equipe.
            </p>
            <button
              className="mt-1 inline-flex min-h-[42px] cursor-pointer items-center justify-center gap-2 rounded-[10px] border border-[#cfddf4] bg-white px-4 text-[12px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => setFormularioAberto(true)}
            >
              <Plus size={16} aria-hidden="true" />
              Criar primeira automação
            </button>
          </section>
        )}

        {!carregando && !erro && resultado && resultado.automacoes.length > 0 && (
          <>
            <section
              className="overflow-hidden rounded-[18px] border border-[#dfe7f1] bg-white shadow-[0_14px_38px_rgba(30,64,175,0.05)]"
              aria-label="Automações da equipe"
            >
              <div className="hidden grid-cols-[minmax(0,1.6fr)_minmax(120px,0.55fr)_minmax(160px,0.65fr)] gap-5 border-b border-[#e7ecf3] bg-[#f8fafd] px-6 py-3.5 text-[10px] font-bold tracking-[0.07em] text-[#7a8799] uppercase min-[701px]:grid">
                <span>Automação</span>
                <span>Status</span>
                <span>Criada em</span>
              </div>

              <ul className="m-0 list-none p-0">
                {resultado.automacoes.map((automacao) => (
                  <li
                    className="grid gap-4 border-b border-[#edf1f6] px-5 py-5 last:border-b-0 min-[701px]:grid-cols-[minmax(0,1.6fr)_minmax(120px,0.55fr)_minmax(160px,0.65fr)] min-[701px]:items-center min-[701px]:gap-5 min-[701px]:px-6"
                    key={automacao.id}
                  >
                    <div className="min-w-0">
                      <strong className="block text-[13.5px] text-[#344055]">
                        {automacao.nome}
                      </strong>
                      <p className="mt-1.5 mb-0 max-w-[620px] text-[11.5px] leading-[1.55] text-[#788599]">
                        {automacao.descricao || "Sem descrição."}
                      </p>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Status
                      </span>
                      <span
                        className={`inline-flex w-fit rounded-full px-2.5 py-1.5 text-[10.5px] font-bold ${classesStatus[automacao.status]}`}
                      >
                        {rotulosStatus[automacao.status]}
                      </span>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Criada em
                      </span>
                      <span className="inline-flex items-center gap-1.5 text-[11.5px] text-[#667388]">
                        <CalendarDays size={14} aria-hidden="true" />
                        {formatarData(automacao.criada_em)}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            </section>

            <nav
              className="mt-5 flex items-center justify-between gap-4 rounded-[14px] border border-[#e1e8f1] bg-white px-4 py-3 max-[520px]:flex-wrap max-[520px]:justify-center"
              aria-label="Paginação de automações"
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
                {resultado.total === 1 ? "automação" : "automações"}
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
