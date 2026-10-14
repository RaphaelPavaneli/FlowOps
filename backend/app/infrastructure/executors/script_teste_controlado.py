import argparse
import os
import time

from app.domain.enums.resultado_teste_controlado import (
    ResultadoTesteControlado,
)
from app.infrastructure.executors.executor_teste_controlado import (
    CODIGO_FALHA_CONTROLADA,
)


def executar(duracao_segundos: float, resultado: ResultadoTesteControlado) -> int:
    """Aguarda o tempo configurado e devolve um resultado determinístico."""
    time.sleep(duracao_segundos)
    if resultado is ResultadoTesteControlado.FALHA:
        return CODIGO_FALHA_CONTROLADA
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duracao-segundos", type=float, required=True)
    parser.add_argument(
        "--resultado",
        choices=[resultado.value for resultado in ResultadoTesteControlado],
        required=True,
    )
    argumentos = parser.parse_args()
    return executar(
        argumentos.duracao_segundos,
        ResultadoTesteControlado(argumentos.resultado),
    )


if __name__ == "__main__":
    # Evita que o depurador pause a falha controlada como SystemExit.
    os._exit(main())
