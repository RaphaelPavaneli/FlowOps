import { FormEvent, useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAutenticacao } from "../contexts/ContextoAutenticacao";
import { ErroAutenticacao } from "../services/autenticacao";

type EstadoMensagem = "erro" | "sucesso" | null;

const classesCampoLogin =
  "h-[52px] w-full rounded-[13px] border border-[#d7deea] bg-white/90 py-0 pr-12 pl-[46px] text-[14px] text-slate-800 outline-none transition-[border-color,box-shadow,background] duration-150 placeholder:text-[#9aa5b6] enabled:hover:border-[#b9c5d8] focus:border-[#6c93ef] focus:bg-white focus:shadow-[0_0_0_4px_rgba(37,99,235,0.1)] disabled:cursor-wait disabled:opacity-[0.72]";

export function FormularioLogin() {
  const { entrar } = useAutenticacao();
  const navegar = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [senhaVisivel, setSenhaVisivel] = useState(false);
  const [carregando, setCarregando] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [estadoMensagem, setEstadoMensagem] =
    useState<EstadoMensagem>(null);

  async function enviarFormulario(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setMensagem("");
    setEstadoMensagem(null);

    if (!email.trim() || !senha) {
      setMensagem("Preencha o e-mail e a senha para continuar.");
      setEstadoMensagem("erro");
      return;
    }

    setCarregando(true);

    try {
      const usuarioAtual = await entrar({ email: email.trim(), senha });
      setMensagem("Acesso validado com sucesso.");
      setEstadoMensagem("sucesso");
      navegar(
        usuarioAtual.perfil_acesso === "administrador"
          ? "/app/dashboard"
          : "/app",
        { replace: true },
      );
    } catch (erro) {
      setMensagem(
        erro instanceof ErroAutenticacao
          ? erro.message
          : "Ocorreu um erro inesperado. Tente novamente.",
      );
      setEstadoMensagem("erro");
    } finally {
      setCarregando(false);
    }
  }

  function informarRecuperacaoIndisponivel() {
    setMensagem("A recuperação de senha estará disponível em breve.");
    setEstadoMensagem(null);
  }

  return (
    <div className="w-full max-w-[456px] rounded-3xl border border-[rgba(255,255,255,0.82)] bg-[rgba(255,255,255,0.78)] px-[42px] pt-[42px] pb-[30px] shadow-[0_28px_70px_rgba(30,64,175,0.09),0_8px_24px_rgba(15,23,42,0.055),inset_0_1px_0_rgba(255,255,255,0.95)] backdrop-blur-[18px] max-[600px]:rounded-[20px] max-[600px]:px-6 max-[600px]:pt-[34px] max-[600px]:pb-[26px]">
      <div className="mb-8 text-center max-[600px]:mb-7">
        <span className="mb-3.5 inline-flex items-center rounded-full border border-[#dbe8fc] bg-[rgba(239,246,255,0.8)] px-[11px] py-1.5 text-[11px] font-[750] tracking-[0.1em] text-[#315a9f] uppercase">
          Área segura
        </span>
        <h1
          className="m-0 text-[clamp(28px,4vw,34px)] font-[720] leading-[1.18] tracking-[-1.25px] text-flowops-texto"
          id="titulo-login"
        >
          Bem-vindo novamente
        </h1>
        <p className="mx-auto mt-3 mb-0 max-w-[330px] text-[14.5px] leading-[1.6] text-flowops-cinza">
          Entre na sua conta para continuar gerenciando sua operação.
        </p>
      </div>

      <form className="flex flex-col gap-[19px]" onSubmit={enviarFormulario} noValidate>
        <div className="flex flex-col gap-2">
          <label className="text-[13.5px] font-[650] text-[#283449]" htmlFor="email">
            E-mail
          </label>
          <div className="group relative flex items-center text-[#8390a5]">
            <Mail
              className="pointer-events-none absolute left-[15px] z-10 transition-colors group-focus-within:text-flowops-600"
              aria-hidden="true"
              size={19}
              strokeWidth={1.8}
            />
            <input
              className={classesCampoLogin}
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              inputMode="email"
              placeholder="seu@email.com"
              value={email}
              onChange={(evento) => setEmail(evento.target.value)}
              aria-describedby={estadoMensagem === "erro" ? "mensagem-login" : undefined}
              disabled={carregando}
              required
            />
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between gap-4">
            <label className="text-[13.5px] font-[650] text-[#283449]" htmlFor="senha">
              Senha
            </label>
            <button
              className="cursor-pointer border-0 bg-transparent p-0 text-[12.5px] font-semibold text-flowops-700 hover:text-flowops-900 hover:underline hover:underline-offset-[3px]"
              type="button"
              onClick={informarRecuperacaoIndisponivel}
            >
              Esqueceu sua senha?
            </button>
          </div>
          <div className="group relative flex items-center text-[#8390a5]">
            <LockKeyhole
              className="pointer-events-none absolute left-[15px] z-10 transition-colors group-focus-within:text-flowops-600"
              aria-hidden="true"
              size={19}
              strokeWidth={1.8}
            />
            <input
              className={classesCampoLogin}
              id="senha"
              name="senha"
              type={senhaVisivel ? "text" : "password"}
              autoComplete="current-password"
              placeholder="Digite sua senha"
              value={senha}
              onChange={(evento) => setSenha(evento.target.value)}
              aria-describedby={estadoMensagem === "erro" ? "mensagem-login" : undefined}
              disabled={carregando}
              required
            />
            <button
              className="absolute right-2.5 grid size-[34px] cursor-pointer place-items-center rounded-[9px] border-0 bg-transparent p-0 text-[#748197] enabled:hover:bg-[#f0f5ff] enabled:hover:text-flowops-700"
              type="button"
              onClick={() => setSenhaVisivel((visivel) => !visivel)}
              aria-label={senhaVisivel ? "Ocultar senha" : "Mostrar senha"}
              aria-pressed={senhaVisivel}
              disabled={carregando}
            >
              {senhaVisivel ? <EyeOff size={19} /> : <Eye size={19} />}
            </button>
          </div>
        </div>

        <div
          id="mensagem-login"
          className={[
            "flex items-center text-[12.5px] leading-[1.45]",
            mensagem ? "-mt-1 min-h-[19px]" : "-mt-[11px] min-h-0",
            estadoMensagem === "erro"
              ? "text-[#b42318]"
              : estadoMensagem === "sucesso"
                ? "gap-[7px] text-[#16764a]"
                : "text-[#596579]",
          ].join(" ")}
          role={estadoMensagem === "erro" ? "alert" : "status"}
          aria-live="polite"
        >
          {estadoMensagem === "sucesso" && (
            <CheckCircle2 size={17} aria-hidden="true" />
          )}
          {mensagem}
        </div>

        <button
          className="mt-px flex h-[52px] w-full cursor-pointer items-center justify-center gap-2.5 rounded-[13px] border-0 bg-[linear-gradient(110deg,#1d4ed8_0%,#2f6ae8_55%,#3978ed_100%)] text-[14px] font-bold text-white shadow-[0_12px_26px_rgba(37,99,235,0.25)] transition-[transform,box-shadow,filter] duration-150 enabled:hover:-translate-y-px enabled:hover:saturate-[1.08] enabled:hover:shadow-[0_15px_31px_rgba(37,99,235,0.31)] enabled:active:translate-y-0 disabled:cursor-wait disabled:opacity-[0.78]"
          type="submit"
          disabled={carregando}
        >
          <span>{carregando ? "Entrando..." : "Entrar"}</span>
          {carregando ? (
            <span
              className="size-[17px] animate-[spin_700ms_linear_infinite] rounded-full border-2 border-white/40 border-t-white"
              aria-hidden="true"
            />
          ) : (
            <ArrowRight size={19} aria-hidden="true" />
          )}
        </button>
      </form>

      <div className="mt-[25px] flex items-center justify-center gap-[7px] text-[11.5px] text-[#7b8799]">
        <LockKeyhole size={14} aria-hidden="true" />
        <span>Seus dados são protegidos e criptografados</span>
      </div>
    </div>
  );
}
