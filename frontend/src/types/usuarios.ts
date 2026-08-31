import type { PerfilAcesso } from "./autenticacao";

export interface UsuarioAdministracao {
  id: string;
  nome: string;
  email: string;
  perfil_acesso: PerfilAcesso;
  equipe_id: string | null;
  ativo: boolean;
}

export interface ListaUsuariosResponse {
  usuarios: UsuarioAdministracao[];
  pagina: number;
  itens_por_pagina: number;
  total: number;
  total_paginas: number;
}

export interface AlterarPerfilUsuarioRequest {
  perfil_acesso: PerfilAcesso;
}

export interface AlterarStatusUsuarioRequest {
  ativo: boolean;
}
