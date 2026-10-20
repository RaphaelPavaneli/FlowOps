import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import {
  CheckCircle2,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Clock3,
  FilePlus2,
  Filter,
  History,
  LoaderCircle,
  Pause,
  Play,
  Plus,
  RefreshCw,
  Search,
  Workflow,
  X,
} from "lucide-react";
import { Link } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import { ModalConfirmacao } from "../components/ModalConfirmacao";
import {
  ativarAutomacao,
  criarAutomacao,
  ErroAutomacoes,
  listarAutomacoes,
  pausarAutomacao,
} from "../services/automacoes";
import {
  ErroExecucoes,
  iniciarExecucao,
} from "../services/execucoes";
import type {
  Automacao,
  ListaAutomacoesResponse,
  ResumoAutomacoes,
  StatusAutomacao,
} from "../types/automacoes";
import type { Execucao, StatusExecucao } from "../types/execucoes";

const ITENS_POR_PAGINA = 20;
const classesBotaoPaginacao =
  "inline-flex min-h-9 items-center justify-center gap-1.5 rounded-lg border border-[#d8dee8] bg-white px-3 text-xs font-semibold text-[#526077] transition-colors enabled:cursor-pointer enabled:hover:border-[#b8c6d9] enabled:hover:bg-[#f7f9fc] enabled:hover:text-flowops-700 disabled:cursor-not-allowed disabled:opacity-45";

const rotulosStatus: Record<StatusAutomacao, string> = {
  rascunho: "Rascunho",
  ativa: "Ativa",
  pausada: "Pausada",
};

const classesStatus: Record<StatusAutomacao, string> = {
  rascunho: "bg-[#eef1f5] text-[#5f6c80]",
  ativa: "bg-[#e9f8ef] text-[#1f7644]",
  pausada: "bg-[#fff4db] text-[#8a6218]",
};

const rotulosStatusExecucao: Record<StatusExecucao, string> = {
  pendente: "Pendente",
  processando: "Processando",
  concluida: "Concluída",
  falhou: "Falhou",
  cancelada: "Cancelada",
};

const classesStatusExecucao: Record<StatusExecucao, string> = {
  pendente: "bg-[#eef1f5] text-[#5f6c80]",
  processando: "bg-[#eaf2ff] text-[#1f5fbf]",
  concluida: "bg-[#e9f8ef] text-[#1f7644]",
  falhou: "bg-[#fff0ef] text-[#a13a32]",
  cancelada: "bg-[#fff4db] text-[#8a6218]",
};

const STATUS_EXECUCAO_ATIVOS = new Set<StatusExecucao>([
  "pendente",
  "processando",
]);
const STATUS_AUTOMACAO_DISPONIVEIS: StatusAutomacao[] = [
  "ativa",
  "pausada",
  "rascunho",
];

function formatarData(data: string) {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(data));
}

function formatarDuracao(execucao: Execucao | null) {
  if (!execucao?.iniciada_em) {
    return "—";
  }

  if (!execucao.finalizada_em) {
    return execucao.status === "processando" ? "Em andamento" : "—";
  }

  const inicio = new Date(execucao.iniciada_em).getTime();
  const fim = new Date(execucao.finalizada_em).getTime();
  const totalSegundos = Math.max(0, Math.floor((fim - inicio) / 1000));
  const horas = Math.floor(totalSegundos / 3600);
  const minutos = Math.floor((totalSegundos % 3600) / 60);
  const segundos = totalSegundos % 60;

  if (horas > 0) {
    return `${horas} h ${minutos} min`;
  }
  if (minutos > 0) {
    return `${minutos} min ${segundos} s`;
  }
  return `${segundos} s`;
}

function BreadcrumbAutomacoes() {
  return (
    <nav className="mb-5" aria-label="Breadcrumb">
      <ol className="m-0 flex list-none items-center gap-2 p-0 text-xs font-semibold">
        <li>
          <Link
            className="text-[#75849a] no-underline transition-colors hover:text-flowops-700 focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-flowops-500"
            to="/app/dashboard"
          >
            Operação
          </Link>
        </li>
        <li className="text-[#a4afbf]" aria-hidden="true">
          /
        </li>
        <li className="text-flowops-texto" aria-current="page">
          Automações
        </li>
      </ol>
    </nav>
  );
}

function FaixaResumoAutomacoes({ resumo }: { resumo: ResumoAutomacoes }) {
  const itens = [
    { rotulo: "Total", valor: resumo.total, cor: "text-flowops-texto" },
    { rotulo: "Ativas", valor: resumo.ativas, cor: "text-[#237a45]" },
    { rotulo: "Pausadas", valor: resumo.pausadas, cor: "text-[#9a6a13]" },
    {
      rotulo: "Rascunhos",
      valor: resumo.rascunhos,
      cor: "text-[#657287]",
    },
  ];
  const classesSeparadores = [
    "border-r border-b sm:border-r-0 sm:border-b-0",
    "border-b sm:border-b-0 sm:border-l",
    "border-r sm:border-r-0 sm:border-l",
    "sm:border-l",
  ];

  return (
    <section
      className="mb-5 overflow-hidden rounded-[10px] border border-[#dfe5ec] bg-white"
      aria-label="Resumo das automações"
    >
      <dl className="m-0 grid grid-cols-2 sm:grid-cols-4">
        {itens.map((item, indice) => (
          <div
            className={`flex min-h-16 flex-col justify-center border-[#e4e8ee] px-4 py-2.5 sm:px-5 ${classesSeparadores[indice]}`}
            key={item.rotulo}
          >
            <dt className="text-[11px] font-semibold text-[#75849a]">
              {item.rotulo}
            </dt>
            <dd className={`m-0 mt-0.5 text-xl leading-none font-bold ${item.cor}`}>
              {item.valor}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

export function PaginaAutomacoes() {
  const { token, usuario, sair } = useAutenticacao();
  const [pagina, setPagina] = useState(1);
  const [buscaDigitada, setBuscaDigitada] = useState("");
  const [buscaAplicada, setBuscaAplicada] = useState("");
  const [statusSelecionados, setStatusSelecionados] = useState<
    StatusAutomacao[]
  >([]);
  const [filtroStatusAberto, setFiltroStatusAberto] = useState(false);
  const [resultado, setResultado] = useState<ListaAutomacoesResponse | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [formularioAberto, setFormularioAberto] = useState(false);
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [salvando, setSalvando] = useState(false);
  const [alterandoStatusId, setAlterandoStatusId] = useState<string | null>(null);
  const [executandoId, setExecutandoId] = useState<string | null>(null);
  const [confirmacaoStatus, setConfirmacaoStatus] = useState<{
    automacao: Automacao;
    acao: "ativar" | "pausar";
  } | null>(null);
  const [automacaoParaExecutar, setAutomacaoParaExecutar] =
    useState<Automacao | null>(null);
  const [mensagemAcao, setMensagemAcao] = useState<{
    tipo: "sucesso" | "erro";
    texto: string;
  } | null>(null);
  const filtroStatusRef = useRef<HTMLDivElement>(null);
  const botaoFiltroStatusRef = useRef<HTMLButtonElement>(null);
  const requisicaoAtualRef = useRef(0);
  const requisicaoCarregamentoRef = useRef(0);

  useEffect(() => {
    document.title = "Automações | FlowOps";
  }, []);

  useEffect(() => {
    const temporizador = window.setTimeout(() => {
      const buscaNormalizada = buscaDigitada.trim().replace(/\s+/g, " ");
      if (buscaNormalizada === buscaAplicada) {
        return;
      }
      setPagina(1);
      setBuscaAplicada(buscaNormalizada);
    }, 350);

    return () => window.clearTimeout(temporizador);
  }, [buscaDigitada, buscaAplicada]);

  useEffect(() => {
    if (!filtroStatusAberto) {
      return;
    }

    const fecharAoClicarFora = (evento: PointerEvent) => {
      if (
        filtroStatusRef.current &&
        !filtroStatusRef.current.contains(evento.target as Node)
      ) {
        setFiltroStatusAberto(false);
      }
    };
    const fecharComEscape = (evento: KeyboardEvent) => {
      if (evento.key === "Escape") {
        setFiltroStatusAberto(false);
        botaoFiltroStatusRef.current?.focus();
      }
    };

    document.addEventListener("pointerdown", fecharAoClicarFora);
    document.addEventListener("keydown", fecharComEscape);
    return () => {
      document.removeEventListener("pointerdown", fecharAoClicarFora);
      document.removeEventListener("keydown", fecharComEscape);
    };
  }, [filtroStatusAberto]);

  const carregarAutomacoes = useCallback(async (silencioso = false) => {
    if (!token || !usuario?.equipe_id) {
      setCarregando(false);
      setResultado(null);
      setErro("");
      return;
    }

    const requisicaoAtual = ++requisicaoAtualRef.current;

    if (!silencioso) {
      requisicaoCarregamentoRef.current = requisicaoAtual;
      setCarregando(true);
      setErro("");
    }

    try {
      const novoResultado = await listarAutomacoes(
        token,
        pagina,
        ITENS_POR_PAGINA,
        {
          busca: buscaAplicada,
          status: statusSelecionados,
        },
      );
      if (requisicaoAtual === requisicaoAtualRef.current) {
        setResultado(novoResultado);
      }
    } catch (falha) {
      if (falha instanceof ErroAutomacoes && falha.status === 401) {
        sair();
        return;
      }

      if (!silencioso && requisicaoAtual === requisicaoAtualRef.current) {
        setErro(
          falha instanceof ErroAutomacoes
            ? falha.message
            : "Ocorreu um erro inesperado ao carregar as automações.",
        );
      }
    } finally {
      if (
        !silencioso &&
        requisicaoAtual === requisicaoCarregamentoRef.current
      ) {
        setCarregando(false);
      }
    }
  }, [
    token,
    usuario?.equipe_id,
    pagina,
    buscaAplicada,
    statusSelecionados,
    sair,
  ]);

  useEffect(() => {
    void carregarAutomacoes();
  }, [carregarAutomacoes]);

  const possuiExecucaoAtiva = resultado?.automacoes.some(
    (automacao) =>
      automacao.ultima_execucao !== null &&
      STATUS_EXECUCAO_ATIVOS.has(automacao.ultima_execucao.status),
  );

  useEffect(() => {
    if (!possuiExecucaoAtiva || carregando) {
      return;
    }

    const intervalo = window.setInterval(() => {
      void carregarAutomacoes(true);
    }, 3000);

    return () => window.clearInterval(intervalo);
  }, [carregarAutomacoes, possuiExecucaoAtiva, carregando]);

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

  async function confirmarAlteracaoStatus() {
    if (
      !token ||
      !confirmacaoStatus ||
      alterandoStatusId === confirmacaoStatus.automacao.id ||
      executandoId === confirmacaoStatus.automacao.id
    ) {
      return;
    }

    const { automacao, acao } = confirmacaoStatus;
    setConfirmacaoStatus(null);
    setAlterandoStatusId(automacao.id);
    setMensagemAcao(null);

    try {
      const automacaoAtualizada =
        acao === "ativar"
          ? await ativarAutomacao(token, automacao.id)
          : await pausarAutomacao(token, automacao.id);

      setResultado((atual) =>
        atual
          ? {
              ...atual,
              automacoes: atual.automacoes.map((item) =>
                item.id === automacaoAtualizada.id
                  ? { ...item, ...automacaoAtualizada }
                  : item,
              ),
            }
          : atual,
      );
      setMensagemAcao({
        tipo: "sucesso",
        texto:
          acao === "ativar"
            ? "Automação ativada com sucesso."
            : "Automação pausada com sucesso.",
      });
      await carregarAutomacoes(true);
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
            : "Ocorreu um erro inesperado ao alterar a automação.",
      });
    } finally {
      setAlterandoStatusId(null);
    }
  }

  async function confirmarInicioExecucao() {
    if (
      !token ||
      !automacaoParaExecutar ||
      alterandoStatusId === automacaoParaExecutar.id ||
      executandoId === automacaoParaExecutar.id
    ) {
      return;
    }

    const automacao = automacaoParaExecutar;
    setAutomacaoParaExecutar(null);
    setExecutandoId(automacao.id);
    setMensagemAcao(null);

    try {
      const execucao = await iniciarExecucao(token, automacao.id);
      setResultado((atual) =>
        atual
          ? {
              ...atual,
              automacoes: atual.automacoes.map((item) =>
                item.id === automacao.id
                  ? { ...item, ultima_execucao: execucao }
                  : item,
              ),
            }
          : atual,
      );
      setMensagemAcao({
        tipo: "sucesso",
        texto: `Execução de “${automacao.nome}” solicitada com sucesso.`,
      });
    } catch (falha) {
      if (falha instanceof ErroExecucoes && falha.status === 401) {
        sair();
        return;
      }

      setMensagemAcao({
        tipo: "erro",
        texto:
          falha instanceof ErroExecucoes
            ? falha.message
            : "Ocorreu um erro inesperado ao solicitar a execução.",
      });
    } finally {
      setExecutandoId(null);
    }
  }

  function alternarStatusFiltro(status: StatusAutomacao) {
    setPagina(1);
    setStatusSelecionados((atuais) =>
      atuais.includes(status)
        ? atuais.filter((item) => item !== status)
        : [...atuais, status],
    );
  }

  function limparBusca() {
    setBuscaDigitada("");
    setBuscaAplicada("");
    setPagina(1);
  }

  function limparFiltros() {
    setBuscaDigitada("");
    setBuscaAplicada("");
    setStatusSelecionados([]);
    setFiltroStatusAberto(false);
    setPagina(1);
  }

  const totalPaginas = Math.max(resultado?.total_paginas ?? 1, 1);
  const filtrosAtivos = buscaAplicada !== "" || statusSelecionados.length > 0;

  if (usuario?.equipe_id === null) {
    return (
      <main className="min-h-screen bg-flowops-app">
        <div className="mx-auto w-full max-w-[1320px] px-4 py-8 sm:px-6 lg:px-8 lg:py-9">
          <BreadcrumbAutomacoes />

          <section className="mb-6">
            <h1 className="m-0 text-[28px] leading-tight font-bold tracking-[-0.6px] text-flowops-texto">
              Automações
            </h1>
            <p className="mt-2 mb-0 max-w-[630px] text-sm leading-6 text-flowops-cinza">
              As automações ficam disponíveis depois que sua conta entra em uma
              equipe.
            </p>
          </section>

          <section
            className="flex min-h-[280px] flex-col items-center justify-center gap-3 rounded-[10px] border border-[#eadfbf] bg-white p-8 text-center"
            aria-labelledby="titulo-automacoes-sem-equipe"
          >
            <span
              className="grid size-11 place-items-center rounded-lg bg-[#fff5d8] text-[#8a6724]"
              aria-hidden="true"
            >
              <Clock3 size={22} />
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
              className="mt-2 inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg border border-[#cbd7e8] bg-white px-4 text-xs font-semibold text-flowops-700 hover:bg-flowops-50"
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
    <main className="min-h-screen bg-flowops-app">
      <div className="mx-5 mt-4 w-full max-w-[1320px] px-4 py-8 sm:px-6 lg:px-8 lg:py-9">
        <BreadcrumbAutomacoes />

        <section className="mb-6 flex items-end justify-between gap-5 max-[640px]:flex-col max-[640px]:items-start">
          <div>
            <h1 className="m-0 text-[28px] leading-tight font-bold tracking-[-0.6px] text-flowops-texto">
              Automações
            </h1>
            <p className="mt-2 mb-0 max-w-[630px] text-sm leading-6 text-flowops-cinza">
              Cadastre e acompanhe as automações compartilhadas com a sua equipe.
            </p>
          </div>

          <button
            className="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg border border-flowops-700 bg-flowops-700 px-4 text-xs font-bold text-white transition-colors hover:bg-flowops-800 disabled:cursor-not-allowed disabled:opacity-55"
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

        {!carregando && !erro && resultado && (
          <FaixaResumoAutomacoes resumo={resultado.resumo} />
        )}

        {formularioAberto && (
          <section className="mb-5 rounded-[10px] border border-[#ccd9e9] bg-white p-5 max-[600px]:p-4">
            <div className="mb-4 flex items-start justify-between gap-4">
              <div>
                <h2 className="m-0 text-base font-bold text-flowops-texto">
                  Criar automação
                </h2>
                <p className="mt-1 mb-0 text-xs leading-5 text-flowops-cinza">
                  A equipe, o criador e o status inicial serão definidos pelo sistema.
                </p>
              </div>
              <button
                className="grid size-8 shrink-0 cursor-pointer place-items-center rounded-lg border border-[#dde5ef] bg-white text-[#69768a] hover:bg-[#f5f7fa]"
                type="button"
                aria-label="Fechar formulário"
                disabled={salvando}
                onClick={fecharFormulario}
              >
                <X size={17} aria-hidden="true" />
              </button>
            </div>

            <form className="grid gap-3.5" onSubmit={enviarFormulario}>
              <label className="grid gap-1.5">
                <span className="text-xs font-semibold text-[#455268]">Nome</span>
                <input
                  className="min-h-10 rounded-lg border border-[#d6dde7] bg-white px-3 text-[13px] text-flowops-texto outline-none transition-colors focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:bg-[#f4f6f8]"
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
                <span className="text-xs font-semibold text-[#455268]">
                  Descrição <span className="font-normal text-[#8995a5]">(opcional)</span>
                </span>
                <textarea
                  className="min-h-20 resize-y rounded-lg border border-[#d6dde7] bg-white px-3 py-2.5 text-[13px] leading-5 text-flowops-texto outline-none transition-colors focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:bg-[#f4f6f8]"
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
                  className="m-0 rounded-lg border border-[#ecd8d6] bg-[#fff7f6] px-3 py-2.5 text-xs font-semibold text-[#8f3029]"
                  role="alert"
                >
                  {mensagemAcao.texto}
                </p>
              )}

              <div className="flex justify-end gap-2.5 max-[480px]:flex-col-reverse">
                <button
                  className="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg border border-[#d6dde7] bg-white px-4 text-xs font-semibold text-[#5e6c80] hover:bg-[#f6f8fa] disabled:cursor-not-allowed disabled:opacity-55"
                  type="button"
                  disabled={salvando}
                  onClick={fecharFormulario}
                >
                  Cancelar
                </button>
                <button
                  className="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg border border-flowops-700 bg-flowops-700 px-4 text-xs font-bold text-white hover:bg-flowops-800 disabled:cursor-not-allowed disabled:opacity-55"
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
            className="mb-4 flex items-center gap-2.5 rounded-lg border border-[#ccebd7] bg-[#f0fdf4] px-3.5 py-2.5 text-xs font-semibold text-[#237a45]"
            role="status"
          >
            <CheckCircle2 size={17} aria-hidden="true" />
            {mensagemAcao.texto}
          </div>
        )}

        {!formularioAberto && mensagemAcao?.tipo === "erro" && (
          <div
            className="mb-4 rounded-lg border border-[#ecd8d6] bg-[#fff7f6] px-3.5 py-2.5 text-xs font-semibold text-[#8f3029]"
            role="alert"
          >
            {mensagemAcao.texto}
          </div>
        )}

        <section
          className="mb-4 flex items-center gap-2.5 max-[640px]:flex-wrap"
          aria-label="Busca e filtros de automações"
        >
          <div className="relative min-w-0 flex-1 max-[640px]:w-full max-[640px]:flex-none">
            <Search
              className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-[#7b8798]"
              size={16}
              aria-hidden="true"
            />
            <input
              className="min-h-10 w-full rounded-lg border border-[#d6dde7] bg-white pr-10 pl-9 text-[13px] text-flowops-texto outline-none transition-colors placeholder:text-[#939eae] focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100"
              type="search"
              value={buscaDigitada}
              maxLength={120}
              aria-label="Buscar automação por nome"
              placeholder="Buscar por nome"
              onChange={(evento) => setBuscaDigitada(evento.target.value)}
            />
            {buscaDigitada && (
              <button
                className="absolute top-1/2 right-2 grid size-7 -translate-y-1/2 cursor-pointer place-items-center rounded-md border-0 bg-transparent text-[#7b8798] hover:bg-[#f1f4f8] hover:text-flowops-texto"
                type="button"
                aria-label="Limpar busca"
                onClick={limparBusca}
              >
                <X size={15} aria-hidden="true" />
              </button>
            )}
          </div>

          <div className="relative" ref={filtroStatusRef}>
            <button
              className={`inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg border bg-white px-3.5 text-xs font-semibold transition-colors ${
                statusSelecionados.length > 0
                  ? "border-flowops-400 text-flowops-700"
                  : "border-[#d6dde7] text-[#526077] hover:border-[#b8c6d9] hover:text-flowops-700"
              }`}
              type="button"
              ref={botaoFiltroStatusRef}
              aria-expanded={filtroStatusAberto}
              aria-controls="filtros-status-automacoes"
              onClick={() => setFiltroStatusAberto((aberto) => !aberto)}
            >
              <Filter size={15} aria-hidden="true" />
              Status
              {statusSelecionados.length > 0 && (
                <span className="grid size-5 place-items-center rounded-full bg-flowops-700 text-[10px] font-bold text-white">
                  {statusSelecionados.length}
                </span>
              )}
              <ChevronDown
                className={`transition-transform ${
                  filtroStatusAberto ? "rotate-180" : ""
                }`}
                size={14}
                aria-hidden="true"
              />
            </button>

            {filtroStatusAberto && (
              <div
                className="absolute top-[calc(100%_+_6px)] right-0 z-30 w-48 rounded-lg border border-[#d8e0ea] bg-white p-2 shadow-[0_10px_28px_rgba(15,39,73,0.14)]"
                id="filtros-status-automacoes"
                role="group"
                aria-label="Filtrar por status"
              >
                <span className="block px-2 py-1.5 text-[10px] font-bold tracking-[0.06em] text-[#7a8799] uppercase">
                  Filtrar por status
                </span>
                {STATUS_AUTOMACAO_DISPONIVEIS.map((status) => (
                  <label
                    className="flex min-h-9 cursor-pointer items-center gap-2.5 rounded-md px-2 text-xs font-medium text-[#3f4d62] hover:bg-[#f4f7fb]"
                    key={status}
                  >
                    <input
                      className="size-4 accent-flowops-700"
                      type="checkbox"
                      checked={statusSelecionados.includes(status)}
                      onChange={() => alternarStatusFiltro(status)}
                    />
                    {rotulosStatus[status]}
                  </label>
                ))}
              </div>
            )}
          </div>

          {filtrosAtivos && (
            <button
              className="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg border-0 bg-transparent px-2 text-xs font-semibold text-[#647287] hover:text-flowops-700"
              type="button"
              onClick={limparFiltros}
            >
              Limpar filtros
            </button>
          )}
        </section>

        {carregando && (
          <section
            className="flex min-h-[260px] flex-col items-center justify-center gap-3 rounded-[10px] border border-[#dfe5ec] bg-white text-center text-flowops-cinza"
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
            className="flex min-h-[260px] flex-col items-center justify-center gap-4 rounded-[10px] border border-[#ecd8d6] bg-white p-8 text-center text-[#8f3029]"
            role="alert"
          >
            <p className="m-0 max-w-[560px] text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg border border-[#cfddf4] bg-white px-4 text-xs font-semibold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => void carregarAutomacoes()}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resultado?.automacoes.length === 0 && (
          <section className="flex min-h-[260px] flex-col items-center justify-center gap-3 rounded-[10px] border border-[#dfe5ec] bg-white p-8 text-center">
            <span className="grid size-11 place-items-center rounded-lg bg-flowops-50 text-flowops-700">
              {filtrosAtivos ? (
                <Search size={22} aria-hidden="true" />
              ) : (
                <Workflow size={22} aria-hidden="true" />
              )}
            </span>
            <h2 className="m-0 text-[17px] text-flowops-texto">
              {filtrosAtivos
                ? "Nenhuma automação encontrada"
                : "Nenhuma automação cadastrada"}
            </h2>
            <p className="m-0 max-w-[480px] text-[13px] leading-[1.6] text-flowops-cinza">
              {filtrosAtivos
                ? "Tente outro nome ou ajuste os status selecionados."
                : "Crie a primeira automação para que ela fique disponível para a sua equipe."}
            </p>
            {filtrosAtivos ? (
              <button
                className="mt-1 inline-flex min-h-10 cursor-pointer items-center justify-center rounded-lg border border-[#cfddf4] bg-white px-4 text-xs font-semibold text-flowops-700 hover:bg-flowops-50"
                type="button"
                onClick={limparFiltros}
              >
                Limpar filtros
              </button>
            ) : (
              <button
                className="mt-1 inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg border border-[#cfddf4] bg-white px-4 text-xs font-semibold text-flowops-700 hover:bg-flowops-50"
                type="button"
                onClick={() => setFormularioAberto(true)}
              >
                <Plus size={16} aria-hidden="true" />
                Criar primeira automação
              </button>
            )}
          </section>
        )}

        {!carregando && !erro && resultado && resultado.automacoes.length > 0 && (
          <>
            <section
              className="overflow-hidden rounded-[10px] border border-[#dfe5ec] bg-white"
              aria-label="Automações da equipe"
            >
              <div className="hidden grid-cols-[minmax(210px,1.35fr)_minmax(88px,0.4fr)_minmax(160px,0.72fr)_minmax(90px,0.38fr)_minmax(260px,0.95fr)] gap-4 border-b border-[#e4e8ee] bg-[#f8f9fb] px-4 py-2.5 text-[10px] font-bold tracking-[0.06em] text-[#7a8799] uppercase min-[960px]:grid lg:px-5">
                <span>Automação</span>
                <span>Status</span>
                <span>Última execução</span>
                <span>Duração</span>
                <span>Ações</span>
              </div>

              <ul className="m-0 list-none p-0">
                {resultado.automacoes.map((automacao) => (
                  <li
                    className="grid gap-3 border-b border-[#edf0f4] px-4 py-2.5 last:border-b-0 hover:bg-[#fafbfd] min-[960px]:grid-cols-[minmax(210px,1.35fr)_minmax(88px,0.4fr)_minmax(160px,0.72fr)_minmax(90px,0.38fr)_minmax(260px,0.95fr)] min-[960px]:items-center min-[960px]:gap-4 lg:px-5"
                    key={automacao.id}
                  >
                    <div className="min-w-0">
                      <strong className="block truncate text-[13px] font-semibold text-[#29364a]">
                        {automacao.nome}
                      </strong>
                      <p className="mt-0.5 mb-0 truncate text-[11px] leading-4 text-[#788599]">
                        {automacao.descricao || "Sem descrição."}
                      </p>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[960px]:sr-only">
                        Status
                      </span>
                      <span
                        className={`inline-flex w-fit rounded-full px-2.5 py-1 text-[10px] font-bold ${classesStatus[automacao.status]}`}
                      >
                        {rotulosStatus[automacao.status]}
                      </span>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[960px]:sr-only">
                        Última execução
                      </span>
                      {automacao.ultima_execucao ? (
                        <div className="min-w-0">
                          <Link
                            className={`inline-flex w-fit rounded-full px-2.5 py-1 text-[10px] font-bold no-underline transition-opacity hover:opacity-75 ${classesStatusExecucao[automacao.ultima_execucao.status]}`}
                            to={`/app/execucoes/${automacao.ultima_execucao.id}`}
                          >
                            {rotulosStatusExecucao[automacao.ultima_execucao.status]}
                          </Link>
                          <span className="mt-1 block text-[10.5px] text-[#788599]">
                            {formatarData(automacao.ultima_execucao.criada_em)}
                          </span>
                        </div>
                      ) : (
                        <span className="text-[11px] text-[#8995a5]">
                          Nunca executada
                        </span>
                      )}
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[960px]:sr-only">
                        Duração
                      </span>
                      <span className="text-[11px] font-medium text-[#526077]">
                        {formatarDuracao(automacao.ultima_execucao)}
                      </span>
                    </div>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[960px]:sr-only">
                        Ações
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        <Link
                          className="inline-flex min-h-8 items-center justify-center gap-1.5 rounded-md border border-[#cfd9e7] bg-white px-2.5 text-[10.5px] font-semibold text-[#49617f] no-underline transition-colors hover:bg-flowops-50 hover:text-flowops-700"
                          to={`/app/automacoes/${automacao.id}/execucoes`}
                          state={{ automacaoNome: automacao.nome }}
                        >
                          <History size={14} aria-hidden="true" />
                          Histórico
                        </Link>

                        {automacao.status === "ativa" && (
                          <button
                            className="inline-flex min-h-8 cursor-pointer items-center justify-center gap-1.5 rounded-md border border-flowops-700 bg-flowops-700 px-2.5 text-[10.5px] font-semibold text-white transition-colors hover:bg-flowops-800 disabled:cursor-not-allowed disabled:opacity-55"
                            type="button"
                            disabled={
                              alterandoStatusId === automacao.id ||
                              executandoId === automacao.id
                            }
                            onClick={() => setAutomacaoParaExecutar(automacao)}
                          >
                            {executandoId === automacao.id ? (
                              <LoaderCircle
                                className="animate-spin"
                                size={14}
                                aria-hidden="true"
                              />
                            ) : (
                              <Play size={14} aria-hidden="true" />
                            )}
                            {executandoId === automacao.id
                              ? "Solicitando..."
                              : "Executar"}
                          </button>
                        )}

                        <button
                          className="inline-flex min-h-8 cursor-pointer items-center justify-center gap-1.5 rounded-md border border-[#cfd9e7] bg-white px-2.5 text-[10.5px] font-semibold text-[#49617f] transition-colors hover:bg-flowops-50 hover:text-flowops-700 disabled:cursor-not-allowed disabled:opacity-55"
                          type="button"
                          disabled={
                            alterandoStatusId === automacao.id ||
                            executandoId === automacao.id
                          }
                          onClick={() =>
                            setConfirmacaoStatus({
                              automacao,
                              acao:
                                automacao.status === "ativa"
                                  ? "pausar"
                                  : "ativar",
                            })
                          }
                        >
                          {alterandoStatusId === automacao.id ? (
                            <LoaderCircle
                              className="animate-spin"
                              size={14}
                              aria-hidden="true"
                            />
                          ) : automacao.status === "ativa" ? (
                            <Pause size={14} aria-hidden="true" />
                          ) : (
                            <Play size={14} aria-hidden="true" />
                          )}
                          {alterandoStatusId === automacao.id
                            ? "Salvando..."
                            : automacao.status === "ativa"
                              ? "Pausar"
                              : "Ativar"}
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </section>

            <nav
              className="mt-4 flex items-center justify-between gap-4 border-t border-[#dfe5ec] pt-4 max-[520px]:flex-wrap max-[520px]:justify-center"
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

              <span className="text-[11px] font-semibold text-[#69768a]">
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

      <ModalConfirmacao
        aberto={confirmacaoStatus !== null}
        titulo={
          confirmacaoStatus?.acao === "pausar"
            ? "Pausar automação"
            : "Ativar automação"
        }
        mensagem={
          confirmacaoStatus?.acao === "pausar"
            ? `Deseja pausar “${confirmacaoStatus.automacao.nome}”? Novas execuções ficarão bloqueadas.`
            : `Deseja ativar “${confirmacaoStatus?.automacao.nome ?? ""}”? Ela ficará disponível para novas execuções.`
        }
        textoConfirmar={
          confirmacaoStatus?.acao === "pausar" ? "Pausar" : "Ativar"
        }
        textoCancelar="Cancelar"
        aoConfirmar={() => void confirmarAlteracaoStatus()}
        aoCancelar={() => setConfirmacaoStatus(null)}
      />

      <ModalConfirmacao
        aberto={automacaoParaExecutar !== null}
        titulo="Iniciar execução"
        mensagem={`Deseja solicitar uma nova execução de “${automacaoParaExecutar?.nome ?? ""}”? Ela será registrada inicialmente como pendente.`}
        textoConfirmar="Executar"
        textoCancelar="Cancelar"
        aoConfirmar={() => void confirmarInicioExecucao()}
        aoCancelar={() => setAutomacaoParaExecutar(null)}
      />
    </main>
  );
}
