from pwdlib import PasswordHash

from app.application.services.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    """Gera e verifica hashes Argon2id com parâmetros recomendados."""

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()
        self._dummy_hash = self._password_hash.hash("senha-interna-nao-utilizavel")

    def gerar_hash(self, senha: str) -> str:
        return self._password_hash.hash(senha)

    def verificar(self, senha: str, senha_hash: str | None) -> bool:
        hash_para_verificar = senha_hash or self._dummy_hash
        senha_valida = self._password_hash.verify(senha, hash_para_verificar)
        return senha_valida and senha_hash is not None
