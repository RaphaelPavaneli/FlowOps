export type StatusAutomacao = "rascunho" | "ativa" | "pausada";

export interface Automacao {
  id: string;
  equipe_id: string;
  criada_por_usuario_id: string;
  nome: string;
  descricao: string | null;
  status: StatusAutomacao;
  criada_em: string;
  atualizada_em: string;
}

export interface CriarAutomacaoRequest {
  nome: string;
  descricao?: string | null;
}

export interface ListaAutomacoesResponse {
  automacoes: Automacao[];
  pagina: number;
  itens_por_pagina: number;
  total: number;
  total_paginas: number;
}
