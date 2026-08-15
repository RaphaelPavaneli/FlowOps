export interface CredenciaisLogin {
  email: string;
  senha: string;
}

export interface TokenAutenticacao {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}
