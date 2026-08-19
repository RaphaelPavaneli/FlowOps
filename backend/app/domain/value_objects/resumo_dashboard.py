from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResumoUsuarios:
    """Indicadores de usuários exibidos no dashboard administrativo."""

    total: int
    ativos: int
    inativos: int
    administradores: int
    comuns: int


@dataclass(frozen=True, slots=True)
class ResumoDashboard:
    """Resumo administrativo independente da API e do banco de dados."""

    usuarios: ResumoUsuarios
