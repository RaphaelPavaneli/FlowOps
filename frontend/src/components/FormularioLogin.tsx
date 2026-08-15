import { FormEvent, useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
} from "lucide-react";

import { autenticar, ErroAutenticacao } from "../services/autenticacao";

type EstadoMensagem = "erro" | "sucesso" | null;

export function FormularioLogin() {
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
      await autenticar({ email: email.trim(), senha });
      setMensagem("Acesso validado com sucesso.");
      setEstadoMensagem("sucesso");
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
    <div className="painel-login">
      <div className="introducao-login">
        <span className="etiqueta-login">Área segura</span>
        <h1 id="titulo-login">Bem-vindo novamente</h1>
        <p>Entre na sua conta para continuar gerenciando sua operação.</p>
      </div>

      <form className="formulario-login" onSubmit={enviarFormulario} noValidate>
        <div className="grupo-campo">
          <label htmlFor="email">E-mail</label>
          <div className="campo-com-icone">
            <Mail aria-hidden="true" size={19} strokeWidth={1.8} />
            <input
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

        <div className="grupo-campo">
          <div className="linha-rotulo">
            <label htmlFor="senha">Senha</label>
            <button
              className="link-recuperacao"
              type="button"
              onClick={informarRecuperacaoIndisponivel}
            >
              Esqueceu sua senha?
            </button>
          </div>
          <div className="campo-com-icone">
            <LockKeyhole aria-hidden="true" size={19} strokeWidth={1.8} />
            <input
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
              className="botao-visibilidade"
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
          className={`mensagem-login ${estadoMensagem ?? "informativa"}`}
          role={estadoMensagem === "erro" ? "alert" : "status"}
          aria-live="polite"
        >
          {estadoMensagem === "sucesso" && (
            <CheckCircle2 size={17} aria-hidden="true" />
          )}
          {mensagem}
        </div>

        <button className="botao-entrar" type="submit" disabled={carregando}>
          <span>{carregando ? "Entrando..." : "Entrar"}</span>
          {carregando ? (
            <span className="indicador-carregamento" aria-hidden="true" />
          ) : (
            <ArrowRight size={19} aria-hidden="true" />
          )}
        </button>
      </form>

      <div className="selo-seguranca">
        <LockKeyhole size={14} aria-hidden="true" />
        <span>Seus dados são protegidos e criptografados</span>
      </div>
    </div>
  );
}
