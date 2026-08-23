import { useCallback, useEffect, useState } from "react";
import {
  ArrowLeft,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  LoaderCircle,
  Power,
  RefreshCw,
  Save,
  ShieldCheck,
  UserCheck,
  UsersRound,
  UserX,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import {
  alterarPerfilUsuario,
  alterarStatusUsuario,
  ErroUsuarios,
  listarUsuarios,
} from "../services/usuarios";
import type { PerfilAcesso } from "../types/autenticacao";
import type {
  ListaUsuariosResponse,
  UsuarioAdministracao,
} from "../types/usuarios";

const ITENS_POR_PAGINA = 20;
const classesBotaoPaginacao =
  "inline-flex min-h-10 items-center justify-center gap-1.5 rounded-[10px] border border-[#d6e0ee] bg-white px-3.5 text-[12px] font-bold text-[#526077] transition-colors enabled:cursor-pointer enabled:hover:border-[#adc4e8] enabled:hover:bg-flowops-50 enabled:hover:text-flowops-700 disabled:cursor-not-allowed disabled:opacity-45";

function formatarPerfil(perfil: "administrador" | "usuario") {
  return perfil === "administrador" ? "Administrador" : "Usuário";
}

export function PaginaGestaoUsuarios() {
  const { token, usuario: usuarioAutenticado, sair } = useAutenticacao();
  const navegar = useNavigate();
  const [pagina, setPagina] = useState(1);
  const [resultado, setResultado] = useState<ListaUsuariosResponse | null>(null);
  const [perfisSelecionados, setPerfisSelecionados] = useState<
    Record<string, PerfilAcesso>
  >({});
  const [usuarioEmAlteracaoId, setUsuarioEmAlteracaoId] = useState<string | null>(
    null,
  );
  const [mensagemAcao, setMensagemAcao] = useState<{
    tipo: "sucesso" | "erro";
    texto: string;
  } | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    document.title = "Gerenciamento de usuários | FlowOps";
  }, []);

  const carregarUsuarios = useCallback(async () => {
    if (!token) {
      return;
    }

    setCarregando(true);
    setErro("");
    setMensagemAcao(null);

    try {
      const resposta = await listarUsuarios(token, pagina, ITENS_POR_PAGINA);
      setResultado(resposta);
      setPerfisSelecionados(
        Object.fromEntries(
          resposta.usuarios.map((usuario) => [
            usuario.id,
            usuario.perfil_acesso,
          ]),
        ),
      );
    } catch (falha) {
      if (falha instanceof ErroUsuarios && falha.status === 401) {
        sair();
        return;
      }

      if (falha instanceof ErroUsuarios && falha.status === 403) {
        navegar("/app/acesso-negado", { replace: true });
        return;
      }

      setErro(
        falha instanceof ErroUsuarios
          ? falha.message
          : "Ocorreu um erro inesperado ao carregar os usuários.",
      );
    } finally {
      setCarregando(false);
    }
  }, [token, pagina, navegar, sair]);

  useEffect(() => {
    void carregarUsuarios();
  }, [carregarUsuarios]);

  function atualizarUsuarioNaLista(usuarioAtualizado: UsuarioAdministracao) {
    setResultado((atual) =>
      atual
        ? {
            ...atual,
            usuarios: atual.usuarios.map((usuario) =>
              usuario.id === usuarioAtualizado.id ? usuarioAtualizado : usuario,
            ),
          }
        : atual,
    );
    setPerfisSelecionados((atuais) => ({
      ...atuais,
      [usuarioAtualizado.id]: usuarioAtualizado.perfil_acesso,
    }));
  }

  function tratarFalhaAlteracao(falha: unknown) {
    if (falha instanceof ErroUsuarios && falha.status === 401) {
      sair();
      return;
    }

    if (falha instanceof ErroUsuarios && falha.status === 403) {
      navegar("/app/acesso-negado", { replace: true });
      return;
    }

    setMensagemAcao({
      tipo: "erro",
      texto:
        falha instanceof ErroUsuarios
          ? falha.message
          : "Ocorreu um erro inesperado ao alterar o usuário.",
    });
  }

  async function confirmarAlteracaoPerfil(usuario: UsuarioAdministracao) {
    if (!token) {
      return;
    }

    const novoPerfil =
      perfisSelecionados[usuario.id] ?? usuario.perfil_acesso;
    if (novoPerfil === usuario.perfil_acesso) {
      return;
    }

    const confirmado = window.confirm(
      `Deseja alterar o perfil de ${usuario.nome} para ${formatarPerfil(novoPerfil)}?`,
    );
    if (!confirmado) {
      return;
    }

    setUsuarioEmAlteracaoId(usuario.id);
    setMensagemAcao(null);

    try {
      const usuarioAtualizado = await alterarPerfilUsuario(
        token,
        usuario.id,
        novoPerfil,
      );
      atualizarUsuarioNaLista(usuarioAtualizado);
      setMensagemAcao({
        tipo: "sucesso",
        texto: `Perfil de ${usuario.nome} alterado com sucesso.`,
      });
    } catch (falha) {
      tratarFalhaAlteracao(falha);
    } finally {
      setUsuarioEmAlteracaoId(null);
    }
  }

  async function confirmarAlteracaoStatus(usuario: UsuarioAdministracao) {
    if (!token) {
      return;
    }

    const novoStatus = !usuario.ativo;
    const acao = novoStatus ? "ativar" : "desativar";
    const confirmado = window.confirm(
      `Deseja ${acao} a conta de ${usuario.nome}?`,
    );
    if (!confirmado) {
      return;
    }

    setUsuarioEmAlteracaoId(usuario.id);
    setMensagemAcao(null);

    try {
      const usuarioAtualizado = await alterarStatusUsuario(
        token,
        usuario.id,
        novoStatus,
      );
      atualizarUsuarioNaLista(usuarioAtualizado);
      setMensagemAcao({
        tipo: "sucesso",
        texto: `Conta de ${usuario.nome} ${novoStatus ? "ativada" : "desativada"} com sucesso.`,
      });
    } catch (falha) {
      tratarFalhaAlteracao(falha);
    } finally {
      setUsuarioEmAlteracaoId(null);
    }
  }

  const totalPaginas = Math.max(resultado?.total_paginas ?? 1, 1);
  const alteracaoEmAndamento = usuarioEmAlteracaoId !== null;

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

        <section className="mb-7 flex items-end justify-between gap-6 max-[700px]:flex-col max-[700px]:items-start">
          <div>
            <span className="mb-2.5 block text-[10.5px] font-bold tracking-[0.1em] text-flowops-700 uppercase">
              Administração
            </span>
            <h1 className="m-0 text-[clamp(30px,4vw,42px)] tracking-[-1.4px] text-flowops-texto">
              Gerenciamento de usuários
            </h1>
            <p className="mt-2.5 mb-0 text-[13.5px] leading-[1.65] text-flowops-cinza">
              Consulte os usuários cadastrados e acompanhe seus acessos.
            </p>
          </div>

          {resultado && (
            <span className="inline-flex items-center gap-2 rounded-[10px] border border-[#dce5f1] bg-white px-3.5 py-2.5 text-[11.5px] font-semibold text-[#5e6c80]">
              <UsersRound size={17} className="text-flowops-600" aria-hidden="true" />
              {resultado.total} {resultado.total === 1 ? "usuário" : "usuários"}
            </span>
          )}
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
            className="flex min-h-[300px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#e0e7f1] bg-white text-center text-flowops-cinza"
            aria-live="polite"
            aria-busy="true"
          >
            <span
              className="size-6 animate-spin rounded-full border-2 border-flowops-600/20 border-t-flowops-600"
              aria-hidden="true"
            />
            <p className="m-0 text-[13px]">Carregando usuários...</p>
          </section>
        )}

        {!carregando && erro && (
          <section
            className="flex min-h-[300px] flex-col items-center justify-center gap-4 rounded-[18px] border border-[#ecd8d6] bg-white p-8 text-center text-[#8f3029]"
            role="alert"
          >
            <p className="m-0 text-[13px]">{erro}</p>
            <button
              className="inline-flex min-h-[44px] cursor-pointer items-center justify-center gap-2 rounded-[11px] border border-[#cfddf4] bg-white px-5 text-[13px] font-bold text-flowops-700 hover:bg-flowops-50"
              type="button"
              onClick={carregarUsuarios}
            >
              <RefreshCw size={17} aria-hidden="true" />
              Tentar novamente
            </button>
          </section>
        )}

        {!carregando && !erro && resultado && resultado.usuarios.length === 0 && (
          <section className="flex min-h-[300px] flex-col items-center justify-center gap-3 rounded-[18px] border border-[#e0e7f1] bg-white p-8 text-center">
            <UsersRound size={30} className="text-[#8794a8]" aria-hidden="true" />
            <h2 className="m-0 text-[17px] text-flowops-texto">Nenhum usuário encontrado</h2>
            <p className="m-0 text-[13px] text-flowops-cinza">
              Ainda não existem usuários para apresentar nesta página.
            </p>
          </section>
        )}

        {!carregando && !erro && resultado && resultado.usuarios.length > 0 && (
          <>
            <section
              className="overflow-hidden rounded-[18px] border border-[#dfe7f1] bg-white shadow-[0_14px_38px_rgba(30,64,175,0.05)]"
              aria-label="Usuários cadastrados"
            >
              <div className="hidden grid-cols-[minmax(0,1.25fr)_minmax(0,1.45fr)_minmax(150px,0.8fr)_minmax(90px,0.5fr)_minmax(190px,0.9fr)] gap-4 border-b border-[#e7ecf3] bg-[#f8fafd] px-6 py-3.5 text-[10px] font-bold tracking-[0.07em] text-[#7a8799] uppercase min-[701px]:grid">
                <span>Usuário</span>
                <span>E-mail</span>
                <span>Perfil</span>
                <span>Status</span>
                <span>Ações</span>
              </div>

              <ul className="m-0 list-none p-0">
                {resultado.usuarios.map((usuario) => {
                  const propriaConta = usuario.id === usuarioAutenticado?.id;
                  const perfilSelecionado =
                    perfisSelecionados[usuario.id] ?? usuario.perfil_acesso;
                  const perfilFoiAlterado =
                    perfilSelecionado !== usuario.perfil_acesso;
                  const alterandoEsteUsuario =
                    usuarioEmAlteracaoId === usuario.id;

                  return (
                    <li
                      className="grid gap-4 border-b border-[#edf1f6] px-5 py-5 last:border-b-0 min-[701px]:grid-cols-[minmax(0,1.25fr)_minmax(0,1.45fr)_minmax(150px,0.8fr)_minmax(90px,0.5fr)_minmax(190px,0.9fr)] min-[701px]:items-center min-[701px]:gap-4 min-[701px]:px-6 min-[701px]:py-[17px]"
                      key={usuario.id}
                    >
                    <div className="flex min-w-0 items-center gap-3">
                      <span className="grid size-9 shrink-0 place-items-center rounded-[11px] bg-flowops-50 text-[11px] font-bold text-flowops-700">
                        {usuario.nome.trim().charAt(0).toUpperCase()}
                      </span>
                      <div className="min-w-0">
                        <strong className="block overflow-hidden text-ellipsis text-[13px] text-[#344055]">
                          {usuario.nome}
                        </strong>
                        {propriaConta && (
                          <small className="mt-0.5 block text-[10px] font-semibold text-flowops-600">
                            Sua conta
                          </small>
                        )}
                      </div>
                    </div>

                    <span className="min-w-0 overflow-hidden text-ellipsis text-[12.5px] text-[#667388]">
                      {usuario.email}
                    </span>

                    <label className="grid gap-1.5">
                      <span className="text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Perfil
                      </span>
                      <select
                        className="min-h-10 w-full rounded-[10px] border border-[#d6e0ee] bg-white px-2.5 text-[11.5px] font-semibold text-[#526077] outline-none transition-colors focus:border-flowops-500 focus:ring-2 focus:ring-flowops-100 disabled:cursor-not-allowed disabled:bg-[#f3f5f8] disabled:text-[#8a95a5]"
                        aria-label={`Perfil de ${usuario.nome}`}
                        value={perfilSelecionado}
                        disabled={propriaConta || alteracaoEmAndamento}
                        onChange={(evento) =>
                          setPerfisSelecionados((atuais) => ({
                            ...atuais,
                            [usuario.id]: evento.target.value as PerfilAcesso,
                          }))
                        }
                      >
                        <option value="usuario">Usuário</option>
                        <option value="administrador">Administrador</option>
                      </select>
                    </label>

                    <div>
                      <span className="mb-1.5 block text-[10px] font-bold tracking-[0.05em] text-[#7a8799] uppercase min-[701px]:sr-only">
                        Status
                      </span>
                      <span
                        className={`inline-flex w-fit items-center gap-1.5 rounded-full px-2.5 py-1.5 text-[10.5px] font-bold ${
                          usuario.ativo
                            ? "bg-[#ecfdf3] text-[#237a45]"
                            : "bg-[#fff1f0] text-[#a33a32]"
                        }`}
                      >
                        {usuario.ativo ? (
                          <UserCheck size={13} aria-hidden="true" />
                        ) : (
                          <UserX size={13} aria-hidden="true" />
                        )}
                        {usuario.ativo ? "Ativo" : "Inativo"}
                      </span>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      <button
                        className="inline-flex min-h-9 cursor-pointer items-center justify-center gap-1.5 rounded-[9px] border border-[#cfddf4] bg-white px-3 text-[10.5px] font-bold text-flowops-700 transition-colors enabled:hover:bg-flowops-50 disabled:cursor-not-allowed disabled:opacity-45"
                        type="button"
                        disabled={
                          propriaConta ||
                          !perfilFoiAlterado ||
                          alteracaoEmAndamento
                        }
                        onClick={() => void confirmarAlteracaoPerfil(usuario)}
                      >
                        {alterandoEsteUsuario ? (
                          <LoaderCircle
                            className="animate-spin"
                            size={14}
                            aria-hidden="true"
                          />
                        ) : (
                          <Save size={14} aria-hidden="true" />
                        )}
                        Salvar perfil
                      </button>

                      <button
                        className={`inline-flex min-h-9 cursor-pointer items-center justify-center gap-1.5 rounded-[9px] border px-3 text-[10.5px] font-bold transition-colors disabled:cursor-not-allowed disabled:opacity-45 ${
                          usuario.ativo
                            ? "border-[#ecd8d6] bg-white text-[#9a3b34] enabled:hover:bg-[#fff5f4]"
                            : "border-[#ccebd7] bg-white text-[#237a45] enabled:hover:bg-[#f0fdf4]"
                        }`}
                        type="button"
                        disabled={propriaConta || alteracaoEmAndamento}
                        onClick={() => void confirmarAlteracaoStatus(usuario)}
                      >
                        {alterandoEsteUsuario ? (
                          <LoaderCircle
                            className="animate-spin"
                            size={14}
                            aria-hidden="true"
                          />
                        ) : (
                          <Power size={14} aria-hidden="true" />
                        )}
                        {usuario.ativo ? "Desativar" : "Ativar"}
                      </button>
                    </div>
                    </li>
                  );
                })}
              </ul>
            </section>

            <nav
              className="mt-5 flex items-center justify-between gap-4 rounded-[14px] border border-[#e1e8f1] bg-white px-4 py-3 max-[520px]:flex-wrap max-[520px]:justify-center"
              aria-label="Paginação de usuários"
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
                Página {resultado.pagina} de {totalPaginas}
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
