export interface CredenciaisLogin {
  email: string;
  senha: string;
}

export interface TokenAutenticacao {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}

export type PerfilAcesso = "administrador" | "usuario";

export interface UsuarioAutenticado {
  id: string;
  nome: string;
  email: string;
  perfil_acesso: PerfilAcesso;
  ativo: boolean;
}
