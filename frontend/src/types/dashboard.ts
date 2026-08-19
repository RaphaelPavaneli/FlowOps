export interface ResumoUsuariosDashboard {
  total: number;
  ativos: number;
  inativos: number;
  administradores: number;
  comuns: number;
}

export interface ResumoDashboard {
  usuarios: ResumoUsuariosDashboard;
}
