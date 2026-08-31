import { useEffect, useId, useRef } from "react";
import { createPortal } from "react-dom";

interface PropriedadesModalConfirmacao {
  aberto: boolean;
  mensagem: string;
  aoConfirmar: () => void;
  aoCancelar: () => void;
  titulo?: string;
  textoConfirmar?: string;
  textoCancelar?: string;
}

export function ModalConfirmacao({
  aberto,
  mensagem,
  aoConfirmar,
  aoCancelar,
  titulo = "Confirmar ação",
  textoConfirmar = "Sim",
  textoCancelar = "Não",
}: PropriedadesModalConfirmacao) {
  const tituloId = useId();
  const mensagemId = useId();
  const modalRef = useRef<HTMLDivElement>(null);
  const botaoCancelarRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!aberto) {
      return;
    }

    const elementoFocadoAnterior = document.activeElement as HTMLElement | null;
    const overflowAnterior = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    botaoCancelarRef.current?.focus();

    return () => {
      document.body.style.overflow = overflowAnterior;
      elementoFocadoAnterior?.focus();
    };
  }, [aberto]);

  if (!aberto) {
    return null;
  }

  function tratarTeclado(evento: React.KeyboardEvent<HTMLDivElement>) {
    if (evento.key === "Escape") {
      evento.preventDefault();
      aoCancelar();
      return;
    }

    if (evento.key !== "Tab") {
      return;
    }

    const elementosFocaveis = modalRef.current?.querySelectorAll<HTMLElement>(
      'button:not([disabled])',
    );
    if (!elementosFocaveis?.length) {
      return;
    }

    const primeiro = elementosFocaveis[0];
    const ultimo = elementosFocaveis[elementosFocaveis.length - 1];

    if (evento.shiftKey && document.activeElement === primeiro) {
      evento.preventDefault();
      ultimo.focus();
    } else if (!evento.shiftKey && document.activeElement === ultimo) {
      evento.preventDefault();
      primeiro.focus();
    }
  }

  return createPortal(
    <div
      className="fixed inset-0 z-100 flex items-center justify-center bg-slate-950/45 px-4 py-8 backdrop-blur-[2px]"
      onMouseDown={(evento) => {
        if (evento.target === evento.currentTarget) {
          aoCancelar();
        }
      }}
    >
      <div
        ref={modalRef}
        className="w-full max-w-[430px] rounded-[18px] border border-white/90 bg-white p-6 shadow-[0_28px_80px_rgba(15,23,42,0.24)] sm:p-7"
        role="dialog"
        aria-modal="true"
        aria-labelledby={tituloId}
        aria-describedby={mensagemId}
        onKeyDown={tratarTeclado}
      >
        <h2
          className="m-0 text-[20px] font-bold tracking-[-0.4px] text-flowops-texto"
          id={tituloId}
        >
          {titulo}
        </h2>
        <p
          className="mt-3 mb-0 text-[14px] leading-[1.65] text-flowops-cinza"
          id={mensagemId}
        >
          {mensagem}
        </p>

        <div className="mt-7 flex justify-end gap-3">
          <button
            ref={botaoCancelarRef}
            className="inline-flex min-h-11 min-w-22 cursor-pointer items-center justify-center rounded-xl border border-[#d6e0ee] bg-white px-4 text-[13px] font-bold text-[#526077] transition-colors hover:border-[#adc4e8] hover:bg-flowops-50 hover:text-flowops-700"
            type="button"
            onClick={aoCancelar}
          >
            {textoCancelar}
          </button>
          <button
            className="inline-flex min-h-11 min-w-22 cursor-pointer items-center justify-center rounded-xl border-0 bg-flowops-700 px-4 text-[13px] font-bold text-white shadow-[0_9px_20px_rgba(37,99,235,0.2)] transition-[transform,box-shadow] hover:-translate-y-px hover:shadow-[0_12px_24px_rgba(37,99,235,0.27)]"
            type="button"
            onClick={aoConfirmar}
          >
            {textoConfirmar}
          </button>
        </div>
      </div>
    </div>,
    document.body,
  );
}
