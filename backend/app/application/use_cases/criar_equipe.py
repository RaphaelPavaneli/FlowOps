from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.equipe import Equipe
from app.domain.repositories.equipe_repository import EquipeRepository


class CriarEquipe:
    """Cria uma equipe ativa para agrupar usuários da operação."""

    def __init__(self, equipe_repository: EquipeRepository) -> None:
        self._equipe_repository = equipe_repository

    def executar(self, nome: str) -> Equipe:
        agora = datetime.now(timezone.utc)
        equipe = Equipe(
            id=uuid4(),
            nome=nome.strip(),
            ativa=True,
            criada_em=agora,
            atualizada_em=agora,
        )
        return self._equipe_repository.salvar(equipe)
