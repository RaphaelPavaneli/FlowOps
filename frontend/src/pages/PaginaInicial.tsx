import { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  ArrowRight,
  Boxes,
  CheckCircle2,
  CircleGauge,
  Code2,
  Eye,
  Layers3,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { Marca } from "../components/Marca";

const beneficios = [
  {
    titulo: "Centralização",
    descricao:
      "Reunir processos, atividades e informações importantes em um único ambiente.",
    Icone: Layers3,
  },
  {
    titulo: "Visibilidade",
    descricao:
      "Facilitar o acompanhamento do que está acontecendo em toda a operação.",
    Icone: Eye,
  },
  {
    titulo: "Simplicidade",
    descricao:
      "Oferecer uma experiência clara, objetiva e agradável para quem utiliza.",
    Icone: Sparkles,
  },
];

const tecnologias = [
  "React e TypeScript",
  "FastAPI e Python",
  "SQLAlchemy e SQL Server",
  "JWT, Argon2id e testes",
];

export function PaginaInicial() {
  useEffect(() => {
    document.title = "FlowOps | Gestão empresarial com clareza";
  }, []);

  return (
    <div className="pagina-inicial">
      <a className="atalho-conteudo" href="#conteudo-principal">
        Ir para o conteúdo principal
      </a>

      <header className="cabecalho-home">
        <div className="container cabecalho-home-conteudo">
          <Marca />

          <nav className="navegacao-home" aria-label="Navegação principal">
            <a href="#projeto">O projeto</a>
            <a href="#recursos">Recursos</a>
            <a href="#tecnologias">Tecnologias</a>
          </nav>

          <Link className="botao botao-secundario botao-cabecalho" to="/login">
            Entrar
            <ArrowRight size={17} aria-hidden="true" />
          </Link>
        </div>
      </header>

      <main id="conteudo-principal">
        <section className="secao-hero">
          <div className="decoracao-hero decoracao-hero-um" aria-hidden="true" />
          <div className="decoracao-hero decoracao-hero-dois" aria-hidden="true" />

          <div className="container grade-hero">
            <div className="conteudo-hero">
              <span className="etiqueta-home">
                <Sparkles size={15} aria-hidden="true" />
                Projeto pessoal full-stack
              </span>

              <h1>Gestão empresarial com mais clareza e menos complexidade.</h1>

              <p>
                Organize processos, acompanhe atividades e tenha uma visão
                centralizada da operação da sua empresa em um único lugar.
              </p>

              <div className="acoes-hero">
                <a className="botao botao-primario" href="#projeto">
                  Conhecer o projeto
                </a>
                <Link className="botao botao-link" to="/login">
                  Acessar plataforma
                  <ArrowRight size={18} aria-hidden="true" />
                </Link>
              </div>

              <div className="sinal-confianca">
                <ShieldCheck size={17} aria-hidden="true" />
                Construído com foco em segurança, clareza e evolução contínua.
              </div>
            </div>

            <div className="demonstracao-produto" aria-label="Prévia ilustrativa do FlowOps">
              <div className="topo-demonstracao">
                <div>
                  <span>Visão geral</span>
                  <strong>Resumo da operação</strong>
                </div>
                <span className="status-operacao">
                  <span aria-hidden="true" /> Operação ativa
                </span>
              </div>

              <div className="metricas-demonstracao">
                <article>
                  <span>Processos ativos</span>
                  <strong>08</strong>
                  <small><CheckCircle2 size={13} /> Dentro do fluxo</small>
                </article>
                <article>
                  <span>Atividades de hoje</span>
                  <strong>12</strong>
                  <small><CircleGauge size={13} /> Em acompanhamento</small>
                </article>
              </div>

              <div className="lista-demonstracao">
                <div className="titulo-lista-demonstracao">
                  <span>Fluxos recentes</span>
                  <span>Progresso</span>
                </div>
                <div className="item-demonstracao">
                  <span className="icone-demonstracao"><Boxes size={16} /></span>
                  <div>
                    <strong>Operação comercial</strong>
                    <span>6 de 8 etapas concluídas</span>
                  </div>
                  <span className="porcentagem-demonstracao">75%</span>
                </div>
                <div className="barra-progresso"><span /></div>
              </div>

              <span className="legenda-demonstracao">Dados meramente ilustrativos</span>
            </div>
          </div>
        </section>

        <section className="secao secao-projeto" id="projeto">
          <div className="container grade-projeto">
            <div className="cabecalho-secao">
              <span className="sobretitulo">O propósito</span>
              <h2>Por que o FlowOps foi criado?</h2>
            </div>

            <div className="texto-projeto">
              <p>
                Muitas empresas ainda controlam suas operações usando planilhas
                separadas, mensagens, anotações e sistemas que não conversam
                entre si. Isso dificulta o acompanhamento e aumenta o risco de
                informações importantes se perderem.
              </p>
              <p>
                O FlowOps nasceu como um projeto pessoal para explorar uma
                solução simples e centralizada de gerenciamento empresarial,
                aplicando boas práticas modernas de desenvolvimento full-stack.
              </p>
            </div>
          </div>
        </section>

        <section className="secao secao-recursos" id="recursos">
          <div className="container">
            <div className="cabecalho-secao cabecalho-secao-centralizado">
              <span className="sobretitulo">Objetivos do produto</span>
              <h2>Uma operação mais fácil de compreender</h2>
              <p>
                Três princípios orientam cada decisão de produto e mantêm a
                experiência organizada.
              </p>
            </div>

            <div className="grade-beneficios">
              {beneficios.map(({ titulo, descricao, Icone }) => (
                <article className="cartao-beneficio" key={titulo}>
                  <span className="icone-beneficio"><Icone size={22} /></span>
                  <h3>{titulo}</h3>
                  <p>{descricao}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="secao secao-tecnologias" id="tecnologias">
          <div className="container cartao-tecnologias">
            <div className="conteudo-tecnologias">
              <span className="icone-codigo"><Code2 size={23} /></span>
              <span className="sobretitulo">Construção full-stack</span>
              <h2>Um projeto pessoal desenvolvido do início ao fim</h2>
              <p>
                O FlowOps representa uma jornada de evolução que conecta
                interface, regras de negócio, segurança, banco de dados e boas
                práticas de arquitetura.
              </p>
            </div>

            <ul className="lista-tecnologias">
              {tecnologias.map((tecnologia) => (
                <li key={tecnologia}>
                  <CheckCircle2 size={18} aria-hidden="true" />
                  {tecnologia}
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="secao secao-chamada">
          <div className="container conteudo-chamada">
            <span className="icone-chamada"><CircleGauge size={27} /></span>
            <h2>Pronto para conhecer o FlowOps?</h2>
            <p>Acesse a plataforma e acompanhe a evolução deste projeto.</p>
            <Link className="botao botao-primario" to="/login">
              Acessar plataforma
              <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </div>
        </section>
      </main>

      <footer className="rodape-home">
        <div className="container conteudo-rodape-home">
          <div>
            <Marca />
            <p>Gestão que flui com você.</p>
          </div>
          <p>
            Projeto pessoal desenvolvido para aprendizado e evolução full-stack.
            <br />© {new Date().getFullYear()} FlowOps.
          </p>
        </div>
      </footer>
    </div>
  );
}
