import { Link } from "react-router-dom";

import logoProcessamento from "../assets/branding/logo-processamento.png";

interface PropriedadesMarca {
  clara?: boolean;
}

export function Marca({ clara = false }: PropriedadesMarca) {
  return (
    <Link
      className={`inline-flex items-center gap-[11px] text-[21px] font-[750] tracking-[-0.6px] no-underline ${
        clara ? "text-white" : "text-flowops-900"
      }`}
      to="/"
      aria-label="FlowOps — página inicial"
    >
      <span className="grid size-[38px] shrink-0 place-items-center rounded-[10px] bg-white p-[3px]">
        <img
          className="size-full object-contain"
          src={logoProcessamento}
          alt=""
          aria-hidden="true"
        />
      </span>
      <span>FlowOps</span>
    </Link>
  );
}
