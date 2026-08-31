export interface Equipe {
  id: string;
  nome: string;
  ativa: boolean;
  criada_em: string;
  atualizada_em: string;
}

export interface CriarEquipeRequest {
  nome: string;
}

export interface ListaEquipesResponse {
  equipes: Equipe[];
  pagina: number;
  itens_por_pagina: number;
  total: number;
  total_paginas: number;
}
