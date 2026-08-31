import { FormEvent, useState } from "react";
import {
  ArrowRight,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  UserRound,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import {
  cadastrarUsuario,
  ErroAutenticacao,
} from "../services/autenticacao";

const classesCampoCadastro =
  "h-[52px] w-full rounded-[13px] border border-[#d7deea] bg-white/90 py-0 pr-12 pl-[46px] text-[14px] text-slate-800 outline-none transition-[border-color,box-shadow,background] duration-150 placeholder:text-[#9aa5b6] enabled:hover:border-[#b9c5d8] focus:border-[#6c93ef] focus:bg-white focus:shadow-[0_0_0_4px_rgba(37,99,235,0.1)] disabled:cursor-wait disabled:opacity-[0.72]";
const formatoEmailBasico = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function FormularioCadastro() {
  const navegar = useNavigate();
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmacaoSenha, setConfirmacaoSenha] = useState("");
  const [senhaVisivel, setSenhaVisivel] = useState(false);
  const [confirmacaoVisivel, setConfirmacaoVisivel] = useState(false);
  const [carregando, setCarregando] = useState(false);
  const [mensagem, setMensagem] = useState("");

  async function enviarFormulario(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setMensagem("");

    const nomeLimpo = nome.trim();
    const emailLimpo = email.trim();

    if (!nomeLimpo || !emailLimpo || !senha || !confirmacaoSenha) {
      setMensagem("Preencha todos os campos para criar sua conta.");
      return;
    }

    if (nomeLimpo.length < 2 || nomeLimpo.length > 120) {
      setMensagem("O nome deve possuir entre 2 e 120 caracteres.");
      return;
    }

    if (!formatoEmailBasico.test(emailLimpo)) {
      setMensagem("Informe um e-mail válido para continuar.");
      return;
    }

    if (senha.length < 12 || senha.length > 128) {
      setMensagem("A senha deve possuir entre 12 e 128 caracteres.");
      return;
    }

    if (senha !== confirmacaoSenha) {
      setMensagem("A senha e a confirmação da senha devem ser iguais.");
      return;
    }

    setCarregando(true);

    try {
      await cadastrarUsuario({
        nome: nomeLimpo,
        email: emailLimpo,
        senha,
      });
      navegar("/login", {
        replace: true,
        state: {
          cadastroConcluido: true,
          email: emailLimpo,
        },
      });
    } catch (erro) {
      setMensagem(
        erro instanceof ErroAutenticacao
          ? erro.message
          : "Ocorreu um erro inesperado. Tente novamente.",
      );
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="w-full max-w-[500px] rounded-3xl border border-[rgba(255,255,255,0.82)] bg-[rgba(255,255,255,0.78)] px-[42px] pt-[38px] pb-[28px] shadow-[0_28px_70px_rgba(30,64,175,0.09),0_8px_24px_rgba(15,23,42,0.055),inset_0_1px_0_rgba(255,255,255,0.95)] backdrop-blur-[18px] max-[600px]:rounded-[20px] max-[600px]:px-6 max-[600px]:pt-8 max-[600px]:pb-6">
      <div className="mb-7 text-center">
        <span className="mb-3 inline-flex items-center rounded-full border border-[#dbe8fc] bg-[rgba(239,246,255,0.8)] px-[11px] py-1.5 text-[11px] font-[750] tracking-[0.1em] text-[#315a9f] uppercase">
          Comece agora
        </span>
        <h1
          className="m-0 text-[clamp(28px,4vw,34px)] leading-[1.18] font-[720] tracking-[-1.25px] text-flowops-texto"
          id="titulo-cadastro"
        >
          Crie sua conta
        </h1>
        <p className="mx-auto mt-3 mb-0 max-w-[360px] text-[14.5px] leading-[1.6] text-flowops-cinza">
          Cadastre seus dados para começar a utilizar o FlowOps.
        </p>
      </div>

      <form className="flex flex-col gap-4" onSubmit={enviarFormulario} noValidate>
        <CampoCadastro
          id="cadastro-nome"
          label="Nome"
          type="text"
          autoComplete="name"
          placeholder="Seu nome completo"
          valor={nome}
          alterarValor={setNome}
          Icone={UserRound}
          carregando={carregando}
          mensagemErro={Boolean(mensagem)}
          minLength={2}
          maxLength={120}
        />

        <CampoCadastro
          id="cadastro-email"
          label="E-mail"
          type="email"
          autoComplete="email"
          placeholder="seu@email.com"
          valor={email}
          alterarValor={setEmail}
          Icone={Mail}
          carregando={carregando}
          mensagemErro={Boolean(mensagem)}
        />

        <CampoSenha
          id="cadastro-senha"
          label="Senha"
          placeholder="No mínimo 12 caracteres"
          valor={senha}
          alterarValor={setSenha}
          visivel={senhaVisivel}
          alterarVisibilidade={() => setSenhaVisivel((atual) => !atual)}
          carregando={carregando}
          mensagemErro={Boolean(mensagem)}
        />

        <CampoSenha
          id="cadastro-confirmacao-senha"
          label="Confirmação da senha"
          placeholder="Digite a senha novamente"
          valor={confirmacaoSenha}
          alterarValor={setConfirmacaoSenha}
          visivel={confirmacaoVisivel}
          alterarVisibilidade={() =>
            setConfirmacaoVisivel((atual) => !atual)
          }
          carregando={carregando}
          mensagemErro={Boolean(mensagem)}
        />

        <div
          id="mensagem-cadastro"
          className={[
            "text-[12.5px] leading-[1.45] text-[#b42318]",
            mensagem ? "min-h-[19px]" : "-mt-2 min-h-0",
          ].join(" ")}
          role="alert"
          aria-live="polite"
        >
          {mensagem}
        </div>

        <button
          className="flex h-[52px] w-full cursor-pointer items-center justify-center gap-2.5 rounded-[13px] border-0 bg-[linear-gradient(110deg,#1d4ed8_0%,#2f6ae8_55%,#3978ed_100%)] text-[14px] font-bold text-white shadow-[0_12px_26px_rgba(37,99,235,0.25)] transition-[transform,box-shadow,filter] duration-150 enabled:hover:-translate-y-px enabled:hover:saturate-[1.08] enabled:hover:shadow-[0_15px_31px_rgba(37,99,235,0.31)] enabled:active:translate-y-0 disabled:cursor-wait disabled:opacity-[0.78]"
          type="submit"
          disabled={carregando}
        >
          <span>{carregando ? "Criando conta..." : "Criar conta"}</span>
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

      <p className="mt-5 mb-0 text-center text-[12.5px] text-[#6f7b8e]">
        Já possui uma conta?{" "}
        <Link
          className="font-bold text-flowops-700 no-underline hover:text-flowops-900 hover:underline hover:underline-offset-[3px]"
          to="/login"
        >
          Entrar
        </Link>
      </p>

      <div className="mt-4 flex items-center justify-center gap-[7px] text-[11.5px] text-[#7b8799]">
        <LockKeyhole size={14} aria-hidden="true" />
        <span>Sua conta será criada com perfil de usuário</span>
      </div>
    </div>
  );
}

interface PropriedadesCampoCadastro {
  id: string;
  label: string;
  type: "text" | "email";
  autoComplete: string;
  placeholder: string;
  valor: string;
  alterarValor: (valor: string) => void;
  Icone: typeof UserRound;
  carregando: boolean;
  mensagemErro: boolean;
  minLength?: number;
  maxLength?: number;
}

function CampoCadastro({
  id,
  label,
  type,
  autoComplete,
  placeholder,
  valor,
  alterarValor,
  Icone,
  carregando,
  mensagemErro,
  minLength,
  maxLength,
}: PropriedadesCampoCadastro) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-[13.5px] font-[650] text-[#283449]" htmlFor={id}>
        {label}
      </label>
      <div className="group relative flex items-center text-[#8390a5]">
        <Icone
          className="pointer-events-none absolute left-[15px] z-10 transition-colors group-focus-within:text-flowops-600"
          aria-hidden="true"
          size={19}
          strokeWidth={1.8}
        />
        <input
          className={classesCampoCadastro}
          id={id}
          name={id}
          type={type}
          autoComplete={autoComplete}
          inputMode={type === "email" ? "email" : undefined}
          placeholder={placeholder}
          value={valor}
          onChange={(evento) => alterarValor(evento.target.value)}
          aria-describedby={mensagemErro ? "mensagem-cadastro" : undefined}
          disabled={carregando}
          minLength={minLength}
          maxLength={maxLength}
          required
        />
      </div>
    </div>
  );
}

interface PropriedadesCampoSenha {
  id: string;
  label: string;
  placeholder: string;
  valor: string;
  alterarValor: (valor: string) => void;
  visivel: boolean;
  alterarVisibilidade: () => void;
  carregando: boolean;
  mensagemErro: boolean;
}

function CampoSenha({
  id,
  label,
  placeholder,
  valor,
  alterarValor,
  visivel,
  alterarVisibilidade,
  carregando,
  mensagemErro,
}: PropriedadesCampoSenha) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-[13.5px] font-[650] text-[#283449]" htmlFor={id}>
        {label}
      </label>
      <div className="group relative flex items-center text-[#8390a5]">
        <LockKeyhole
          className="pointer-events-none absolute left-[15px] z-10 transition-colors group-focus-within:text-flowops-600"
          aria-hidden="true"
          size={19}
          strokeWidth={1.8}
        />
        <input
          className={classesCampoCadastro}
          id={id}
          name={id}
          type={visivel ? "text" : "password"}
          autoComplete="new-password"
          placeholder={placeholder}
          value={valor}
          onChange={(evento) => alterarValor(evento.target.value)}
          aria-describedby={mensagemErro ? "mensagem-cadastro" : undefined}
          disabled={carregando}
          minLength={12}
          maxLength={128}
          required
        />
        <button
          className="absolute right-2.5 grid size-[34px] cursor-pointer place-items-center rounded-[9px] border-0 bg-transparent p-0 text-[#748197] enabled:hover:bg-[#f0f5ff] enabled:hover:text-flowops-700"
          type="button"
          onClick={alterarVisibilidade}
          aria-label={visivel ? `Ocultar ${label.toLowerCase()}` : `Mostrar ${label.toLowerCase()}`}
          aria-pressed={visivel}
          disabled={carregando}
        >
          {visivel ? <EyeOff size={19} /> : <Eye size={19} />}
        </button>
      </div>
    </div>
  );
}
