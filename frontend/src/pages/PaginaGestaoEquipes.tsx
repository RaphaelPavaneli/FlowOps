import { FormEvent, useCallback, useEffect, useState } from "react";
import {
  ArrowLeft,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  LoaderCircle,
  Network,
  Plus,
  RefreshCw,
  Save,
  UserRoundCheck,
  UsersRound,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { ModalConfirmacao } from "../components/ModalConfirmacao";
import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import {
  associarUsuarioEquipe,
  criarEquipe,
  ErroEquipes,
  listarEquipes,
} from "../services/equipes";
import { ErroUsuarios, listarUsuarios } from "../services/usuarios";
import type { ListaEquipesResponse } from "../types/equipes";
import type {
  ListaUsuariosResponse,
  UsuarioAdministracao,
} from "../types/usuarios";

const ITENS_USUARIOS_POR_PAGINA = 20;
const classesBotaoPaginacao =
  "inline-flex min-h-10 items-center justify-center gap-1.5 rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 text-[12px] font-bold text-[#526077] transition-colors enabled:cursor-pointer enabled:hover:border-[#adc4e8] enabled:hover:bg-flowops-50 enabled:hover:text-flowops-700 disabled:cursor-not-allowed disabled:opacity-45";

export function PaginaGestaoEquipes() {
  const { token, sair } = useAutenticacao();
  const navegar = useNavigate();
  const [paginaUsuarios, setPaginaUsuarios] = useState(1);
  const [resultadoEquipes, setResultadoEquipes] =
    useState<ListaEquipesResponse | null>(null);
  const [resultadoUsuarios, setResultadoUsuarios] =
    useState<ListaUsuariosResponse | null>(null);
  const [equipesSelecionadas, setEquipesSelecionadas] = useState<
    Record<string, string>
  >({});
  const [nomeEquipe, setNomeEquipe] = useState("");
  const [carregando, setCarregando] = useState(true);
  const [criandoEquipe, setCriandoEquipe] = useState(false);
  const [usuarioEmAssociacaoId, setUsuarioEmAssociacaoId] = useState<
    string | null
  >(null);
  const [associacaoPendente, setAssociacaoPendente] = useState<{
    usuario: UsuarioAdministracao;
    equipeId: string;
    nomeEquipe: string;
  } | null>(null);
  const [erro, setErro] = useState("");
  const [mensagemAcao, setMensagemAcao] = useState<{
    tipo: "sucesso" | "erro";
    texto: string;
  } | null>(null);

  useEffect(() => {
    document.title = "Gestão de equipes | FlowOps";
  }, []);

  const tratarErroAcesso = useCallback(
    (falha: unknown) => {
      const status =
        falha instanceof ErroEquipes || falha instanceof ErroUsuarios
          ? falha.status
          : null;

      if (status === 401) {
        sair();
        return true;
      }

      if (status === 403) {
        navegar("/app/acesso-negado", { replace: true });
        return true;
      }

      return false;
    },
    [navegar, sair],
  );

  const carregarDados = useCallback(async () => {
    if (!token) {
      return;
    }

    setCarregando(true);
    setErro("");

    try {
      const [equipes, usuarios] = await Promise.all([
        listarEquipes(token),
        listarUsuarios(token, paginaUsuarios, ITENS_USUARIOS_POR_PAGINA),
      ]);
      setResultadoEquipes(equipes);
      setResultadoUsuarios(usuarios);
      setEquipesSelecionadas(
        Object.fromEntries(
          usuarios.usuarios.map((usuario) => [
            usuario.id,
            usuario.equipe_id ?? "",
          ]),
        ),
      );
    } catch (falha) {
      if (tratarErroAcesso(falha)) {
        return;
      }

      setErro(
        falha instanceof Error
          ? falha.message
          : "Ocorreu um erro inesperado ao carregar a gestão de equipes.",
      );
    } finally {
      setCarregando(false);
    }
  }, [token, paginaUsuarios, tratarErroAcesso]);

  useEffect(() => {
    void carregarDados();
  }, [carregarDados]);

  async function enviarCriacaoEquipe(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();

    if (!token || criandoEquipe) {
      return;
    }

    const nomeLimpo = nomeEquipe.trim();
    if (nomeLimpo.length < 2) {
      setMensagemAcao({
        tipo: "erro",
        texto: "Informe um nome com pelo menos 2 caracteres.",
      });
      return;
    }

    setCriandoEquipe(true);
    setMensagemAcao(null);

    try {
      const equipeCriada = await criarEquipe(token, { nome: nomeLimpo });
      setResultadoEquipes((atual) =>
        atual
          ? {
              ...atual,
              equipes: [...atual.equipes, equipeCriada].sort((a, b) =>
                a.nome.localeCompare(b.nome, "pt-BR"),
              ),
              total: atual.total + 1,
            }
          : atual,
      );
      setNomeEquipe("");
      setMensagemAcao({
        tipo: "sucesso",
        texto: `Equipe ${equipeCriada.nome} criada com sucesso.`,
      });
    } catch (falha) {
      if (tratarErroAcesso(falha)) {
        return;
      }

      setMensagemAcao({
        tipo: "erro",
        texto:
          falha instanceof Error
            ? falha.message
            : "Ocorreu um erro inesperado ao criar a equipe.",
      });
    } finally {
      setCriandoEquipe(false);
    }
  }

  function atualizarUsuarioNaLista(usuarioAtualizado: UsuarioAdministracao) {
    setResultadoUsuarios((atual) =>
      atual
        ? {
            ...atual,
            usuarios: atual.usuarios.map((usuario) =>
              usuario.id === usuarioAtualizado.id ? usuarioAtualizado : usuario,
            ),
          }
        : atual,
    );
    setEquipesSelecionadas((atuais) => ({
      ...atuais,
      [usuarioAtualizado.id]: usuarioAtualizado.equipe_id ?? "",
    }));
  }

  function solicitarAssociacao(usuario: UsuarioAdministracao) {
    if (!token || usuarioEmAssociacaoId) {
      return;
    }

    const equipeId = equipesSelecionadas[usuario.id] ?? "";
    if (!equipeId || equipeId === usuario.equipe_id) {
      return;
    }

    const equipe = resultadoEquipes?.equipes.find(
      (item) => item.id === equipeId,
    );
    if (!equipe) {
      setMensagemAcao({
        tipo: "erro",
        texto: "Selecione uma equipe válida.",
      });
      return;
    }

    setAssociacaoPendente({
      usuario,
      equipeId,
      nomeEquipe: equipe.nome,
    });
  }

  async function confirmarAssociacao() {
    if (!token || !associacaoPendente) {
      return;
    }

    const { usuario, equipeId, nomeEquipe } = associacaoPendente;
    setAssociacaoPendente(null);

    setUsuarioEmAssociacaoId(usuario.id);
    setMensagemAcao(null);

    try {
      const usuarioAtualizado = await associarUsuarioEquipe(
        token,
        equipeId,
        usuario.id,
      );
      atualizarUsuarioNaLista(usuarioAtualizado);
      setMensagemAcao({
        tipo: "sucesso",
        texto: `${usuario.nome} foi associado à equipe ${nomeEquipe}.`,
      });
    } catch (falha) {
      if (tratarErroAcesso(falha)) {
        return;
      }

      setMensagemAcao({
        tipo: "erro",
        texto:
          falha instanceof Error
            ? falha.message
            : "Ocorreu um erro inesperado ao associar o usuário.",
      });
    } finally {
      setUsuarioEmAssociacaoId(null);
    }
  }

  const totalPaginasUsuarios = Math.max(
    resultadoUsuarios?.total_paginas ?? 1,
    1,
  );
  const equipesAtivas = resultadoEquipes?.equipes.filter(
    (equipe) => equipe.ativa,
  ) ?? [];

  return (
    <main className="min-h-[calc(100vh-77px)] bg-[#f7f9fc] max-[700px]:min-h-[calc(100vh-116px)]">
      <div className="mx-auto w-[calc(100%_-_48px)] max-w-[1160px] py-12 max-[700px]:w-[calc(100%_-_32px)] max-[700px]:py-9">
        <Link
          className="mb-7 inline-flex items-center gap-2 text-[12.5px] font-semibold text-flowops-700 no-underline hover:text-flowops-900"
          to="/app/administracao"
        >
          <ArrowLeft size={17} aria-hidden="true" />
          Voltar para administração
        </Link>

        <section className="mb-7">
          <span className="mb-2.5 block text-[10.5px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
            Administração
          </span>
          <h1 className="m-0 text-[clamp(30px,4vw,42px)] tracking-[-1.4px] text-flowops-texto">
            Gestão de equipes
          </h1>
          <p className="mt-2.5 mb-0 max-w-[670px] text-[13.5px] leading-[1.65] text-flowops-cinza">
            Crie equipes e defina o contexto operacional de cada usuário.
          </p>
        </section>

        {mensagemAcao && (
          <div
            className={`mb-5 flex items-center gap-2.5 rounded-[12px] border px-4 py-3 text-[12.5px] font-semibold ${
              mensagemAcao.tipo === "sucesso"
                ? "border-[#ccebd7] bg-[#f0fdf4] text-[#237a45]"
                : "border-[#ecd8d6] bg-[#fff7f6] text-[#8f3029]"
            }`}
            role={mensagemAcao.tipo === "erro" ? "alert" : "status"}
          >
            {mensagemAcao.tipo === "sucesso" && (
              <CheckCircle2 size={17} aria-hidden="true" />
            )}
            {mensagemAcao.texto}
          </div>
        )}

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
            <p className="m-0 text-[13px]">Carregando equipes e usuários...</p>
          </section>
        )}

        {!carregando && erro && (
          <section
            className="flex min-h-[320px] flex-col items-center justify-center gap-4 rounded-[18px] border border-[#ecd8d6] bg-white p-8 text-center text-[#8f3029]"
            role="alert"
          >
            <p className="m-0 text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-[#cfddf4] bg-white px-5 text-[13px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={() => void carregarDados()}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resultadoEquipes && resultadoUsuarios && (
          <>
            <section className="mb-7 grid grid-cols-[0.75fr_1.25fr] gap-5 max-[820px]:grid-cols-1">
              <article className="rounded-[18px] border border-[#dfe7f1] bg-white p-6 shadow-[0_14px_38px_rgba(30,64,175,0.05)]">
                <span className="mb-4 grid size-11 place-items-center rounded-[13px] bg-flowops-50 text-flowops-700">
                  <Plus size={21} aria-hidden="true" />
                </span>
                <h2 className="m-0 text-[17px] text-flowops-texto">Nova equipe</h2>
                <p className="mt-1.5 mb-5 text-[12px] leading-[1.6] text-flowops-cinza">
                  Toda nova equipe começa ativa e pronta para receber usuários.
                </p>

                <form className="grid gap-3" onSubmit={enviarCriacaoEquipe}>
                  <label className="grid gap-1.5">
                    <span className="text-[11.5px] font-bold text-[#455268]">
                      Nome da equipe
                    </span>
                    <input
                      className="min-h-[44px] rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 text-[13px] text-flowops-texto outline-none focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:bg-[#f4f6f8]"
                      type="text"
                      value={nomeEquipe}
                      minLength={2}
                      maxLength={120}
                      required
                      disabled={criandoEquipe}
                      placeholder="Ex.: Equipe Operacional"
                      onChange={(evento) => setNomeEquipe(evento.target.value)}
                    />
                  </label>
                  <button
                    className="inline-flex min-h-[42px] cursor-pointer items-center justify-center gap-2 rounded-[10px] border border-flowops-700 bg-flowops-700 px-5 text-[12px] font-bold text-white hover:bg-flowops-800 disabled:cursor-not-allowed disabled:opacity-55"
                    type="submit"
                    disabled={criandoEquipe}
                  >
                    {criandoEquipe ? (
                      <LoaderCircle className="animate-spin" size={16} aria-hidden="true" />
                    ) : (
                      <Plus size={16} aria-hidden="true" />
                    )}
                    {criandoEquipe ? "Criando..." : "Criar equipe"}
                  </button>
                </form>
              </article>

              <article className="rounded-[18px] border border-[#dfe7f1] bg-white p-6 shadow-[0_14px_38px_rgba(30,64,175,0.05)]">
                <div className="mb-5 flex items-center justify-between gap-4">
                  <div>
                    <h2 className="m-0 text-[17px] text-flowops-texto">
                      Equipes cadastradas
                    </h2>
                    <p className="mt-1.5 mb-0 text-[12px] text-flowops-cinza">
                      {resultadoEquipes.total}{" "}
                      {resultadoEquipes.total === 1 ? "equipe" : "equipes"}
                    </p>
                  </div>
                  <Network size={23} className="text-flowops-600" aria-hidden="true" />
                </div>

                {resultadoEquipes.equipes.length === 0 ? (
                  <div className="grid min-h-[115px] place-items-center rounded-[12px] border border-dashed border-[#d6e0ee] bg-[#fafbfd] p-5 text-center">
                    <p className="m-0 text-[12.5px] text-flowops-cinza">
                      Nenhuma equipe cadastrada. Crie a primeira ao lado.
                    </p>
                  </div>
                ) : (
                  <ul className="m-0 grid max-h-[230px] list-none gap-2 overflow-y-auto p-0 pr-1">
                    {resultadoEquipes.equipes.map((equipe) => (
                      <li
                        className="flex items-center justify-between gap-4 rounded-[11px] border border-[#e4eaf2] px-3.5 py-3"
                        key={equipe.id}
                      >
                        <span className="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap text-[12.5px] font-semibold text-[#455268]">
                          {equipe.nome}
                        </span>
                        <span
                          className={`shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold ${
                            equipe.ativa
                              ? "bg-[#ecfdf3] text-[#237a45]"
                              : "bg-[#fff1f0] text-[#a33a32]"
                          }`}
                        >
                          {equipe.ativa ? "Ativa" : "Inativa"}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </article>
            </section>

            <section className="overflow-hidden rounded-[18px] border border-[#dfe7f1] bg-white shadow-[0_14px_38px_rgba(30,64,175,0.05)]">
              <div className="flex items-center justify-between gap-4 border-b border-[#e7ecf3] px-6 py-5 max-[600px]:items-start max-[600px]:px-5">
                <div>
                  <h2 className="m-0 text-[17px] text-flowops-texto">
                    Associação de usuários
                  </h2>
                  <p className="mt-1.5 mb-0 text-[12px] text-flowops-cinza">
                    Defina a equipe operacional de cada conta.
                  </p>
                </div>
                <UsersRound size={22} className="shrink-0 text-flowops-600" aria-hidden="true" />
              </div>

              {resultadoUsuarios.usuarios.length === 0 ? (
                <div className="grid min-h-[220px] place-items-center p-8 text-center">
                  <p className="m-0 text-[13px] text-flowops-cinza">
                    Nenhum usuário disponível para associação.
                  </p>
                </div>
              ) : (
                <>
                  <div className="hidden grid-cols-[minmax(0,1.15fr)_minmax(0,1.25fr)_minmax(180px,0.85fr)_minmax(120px,0.55fr)] gap-4 border-b border-[#e7ecf3] bg-[#f8fafd] px-6 py-3.5 text-[10px] font-bold tracking-[0.07em] text-[#7a8799] uppercase min-[701px]:grid">
                    <span>Usuário</span>
                    <span>E-mail</span>
                    <span>Equipe</span>
                    <span>Ação</span>
                  </div>

                  <ul className="m-0 list-none p-0">
                    {resultadoUsuarios.usuarios.map((usuario) => {
                      const equipeSelecionada = equipesSelecionadas[usuario.id] ?? "";
                      const associacaoAlterada =
                        Boolean(equipeSelecionada) &&
                        equipeSelecionada !== usuario.equipe_id;
                      const associandoEsteUsuario =
                        usuarioEmAssociacaoId === usuario.id;

                      return (
                        <li
                          className="grid gap-4 border-b border-[#edf1f6] px-5 py-5 last:border-b-0 min-[701px]:grid-cols-[minmax(0,1.15fr)_minmax(0,1.25fr)_minmax(180px,0.85fr)_minmax(120px,0.55fr)] min-[701px]:items-center min-[701px]:gap-4 min-[701px]:px-6 min-[701px]:py-[17px]"
                          key={usuario.id}
                        >
                          <div className="flex min-w-0 items-center gap-3">
                            <span className="grid size-9 shrink-0 place-items-center rounded-[11px] bg-flowops-50 text-[11px] font-bold text-flowops-700">
                              {usuario.nome.trim().charAt(0).toUpperCase()}
                            </span>
                            <div className="min-w-0">
                              <strong className="block overflow-hidden text-ellipsis whitespace-nowrap text-[13px] text-[#344055]">
                                {usuario.nome}
                              </strong>
                              {!usuario.equipe_id && (
                                <small className="mt-0.5 block text-[10px] font-semibold text-[#a16525]">
                                  Sem equipe
                                </small>
                              )}
                            </div>
                          </div>

                          <span className="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap text-[12.5px] text-[#667388]">
                            {usuario.email}
                          </span>

                          <label className="grid gap-1.5">
                            <span className="text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                              Equipe
                            </span>
                            <select
                              className="min-h-10 w-full rounded-[10px] border border-[#d6e0ee] bg-white px-2.5 text-[11.5px] font-semibold text-[#526077] outline-none focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:cursor-not-allowed disabled:bg-[#f3f5f8]"
                              aria-label={`Equipe de ${usuario.nome}`}
                              value={equipeSelecionada}
                              disabled={
                                equipesAtivas.length === 0 ||
                                usuarioEmAssociacaoId !== null
                              }
                              onChange={(evento) =>
                                setEquipesSelecionadas((atuais) => ({
                                  ...atuais,
                                  [usuario.id]: evento.target.value,
                                }))
                              }
                            >
                              <option value="">Selecione uma equipe</option>
                              {equipesAtivas.map((equipe) => (
                                <option value={equipe.id} key={equipe.id}>
                                  {equipe.nome}
                                </option>
                              ))}
                            </select>
                          </label>

                          <button
                            className="inline-flex min-h-9 cursor-pointer items-center justify-center gap-1.5 rounded-[9px] border border-[#cfddf4] bg-white px-3 text-[10.5px] font-bold text-flowops-700 transition-colors enabled:hover:bg-flowops-50 disabled:cursor-not-allowed disabled:opacity-45"
                            type="button"
                            disabled={
                              !associacaoAlterada ||
                              usuarioEmAssociacaoId !== null
                            }
                            onClick={() => solicitarAssociacao(usuario)}
                          >
                            {associandoEsteUsuario ? (
                              <LoaderCircle className="animate-spin" size={14} aria-hidden="true" />
                            ) : usuario.equipe_id ? (
                              <Save size={14} aria-hidden="true" />
                            ) : (
                              <UserRoundCheck size={14} aria-hidden="true" />
                            )}
                            {usuario.equipe_id ? "Alterar" : "Associar"}
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                </>
              )}
            </section>

            {resultadoUsuarios.usuarios.length > 0 && (
              <nav
                className="mt-5 flex items-center justify-between gap-4 rounded-[14px] border border-[#e1e8f1] bg-white px-4 py-3 max-[520px]:flex-wrap max-[520px]:justify-center"
                aria-label="Paginação de usuários"
              >
                <button
                  className={classesBotaoPaginacao}
                  type="button"
                  disabled={paginaUsuarios <= 1}
                  onClick={() =>
                    setPaginaUsuarios((atual) => Math.max(1, atual - 1))
                  }
                >
                  <ChevronLeft size={16} aria-hidden="true" />
                  Anterior
                </button>

                <span className="text-[11.5px] font-semibold text-[#69768a]">
                  Página {resultadoUsuarios.pagina} de {totalPaginasUsuarios}
                </span>

                <button
                  className={classesBotaoPaginacao}
                  type="button"
                  disabled={paginaUsuarios >= totalPaginasUsuarios}
                  onClick={() => setPaginaUsuarios((atual) => atual + 1)}
                >
                  Próxima
                  <ChevronRight size={16} aria-hidden="true" />
                </button>
              </nav>
            )}
          </>
        )}
      </div>

      <ModalConfirmacao
        aberto={associacaoPendente !== null}
        mensagem={
          associacaoPendente
            ? `Deseja associar ${associacaoPendente.usuario.nome} à equipe ${associacaoPendente.nomeEquipe}?`
            : ""
        }
        aoConfirmar={() => void confirmarAssociacao()}
        aoCancelar={() => setAssociacaoPendente(null)}
      />
    </main>
  );
}
