import type { PerfilAcesso } from "./autenticacao";

export interface UsuarioAdministracao {
  id: string;
  nome: string;
  email: string;
  perfil_acesso: PerfilAcesso;
  ativo: boolean;
}

export interface ListaUsuariosResponse {
  usuarios: UsuarioAdministracao[];
  pagina: number;
  itens_por_pagina: number;
  total: number;
  total_paginas: number;
}
