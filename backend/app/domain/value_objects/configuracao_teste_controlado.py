from dataclasses import dataclass

from app.domain.enums.resultado_teste_controlado import (
    ResultadoTesteControlado,
)


@dataclass(frozen=True, slots=True)
class ConfiguracaoTesteControlado:
    resultado: ResultadoTesteControlado
