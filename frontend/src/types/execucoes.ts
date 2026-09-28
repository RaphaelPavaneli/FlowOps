export type StatusExecucao =
  | "pendente"
  | "processando"
  | "concluida"
  | "falhou";

export interface Execucao {
  id: string;
  automacao_id: string;
  equipe_id: string;
  solicitada_por_usuario_id: string;
  status: StatusExecucao;
  mensagem_erro: string | null;
  criada_em: string;
  iniciada_em: string | null;
  finalizada_em: string | null;
  atualizada_em: string;
}

export interface ListaExecucoesResponse {
  execucoes: Execucao[];
  pagina: number;
  itens_por_pagina: number;
  total: number;
  total_paginas: number;
}
