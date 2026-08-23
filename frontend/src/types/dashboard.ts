export interface ResumoUsuariosDashboardAdministrativo {
  total: number;
  ativos: number;
  inativos: number;
  administradores: number;
  comuns: number;
}

export interface ResumoDashboardAdministrativo {
  usuarios: ResumoUsuariosDashboardAdministrativo;
}
