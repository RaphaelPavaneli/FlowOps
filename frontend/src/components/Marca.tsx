import { Link } from "react-router-dom";

interface PropriedadesMarca {
  clara?: boolean;
}

export function Marca({ clara = false }: PropriedadesMarca) {
  return (
    <Link
      className={`marca${clara ? " marca-clara" : ""}`}
      to="/"
      aria-label="FlowOps — página inicial"
    >
      <span className="simbolo-marca" aria-hidden="true">
        <span />
        <span />
        <span />
      </span>
      <span>FlowOps</span>
    </Link>
  );
}
