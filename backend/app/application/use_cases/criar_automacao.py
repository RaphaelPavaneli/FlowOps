from datetime import datetime, timezone
from uuid import uuid4

from app.application.services.contexto_equipe import (
    obter_equipe_ativa_do_usuario,
)
from app.domain.entities.automacao import Automacao
from app.domain.entities.usuario import Usuario
from app.domain.enums.status_automacao import StatusAutomacao
from app.domain.exceptions.automacoes import AutomacaoNomeDuplicadoError
from app.domain.repositories.automacao_repository import AutomacaoRepository
from app.domain.repositories.equipe_repository import EquipeRepository


class CriarAutomacao:
    """Cria uma automação em rascunho na equipe do usuário atual."""

    def __init__(
        self,
        automacao_repository: AutomacaoRepository,
        equipe_repository: EquipeRepository,
    ) -> None:
        self._automacao_repository = automacao_repository
        self._equipe_repository = equipe_repository

    def executar(
        self,
        usuario: Usuario,
        nome: str,
        descricao: str | None,
    ) -> Automacao:
        equipe = obter_equipe_ativa_do_usuario(
            usuario,
            self._equipe_repository,
        )
        nome_limpo = " ".join(nome.split())
        nome_normalizado = nome_limpo.casefold()
        if self._automacao_repository.buscar_por_nome_normalizado(
            equipe.id,
            nome_normalizado,
        ):
            raise AutomacaoNomeDuplicadoError

        descricao_limpa = descricao.strip() if descricao else None
        agora = datetime.now(timezone.utc)
        automacao = Automacao(
            id=uuid4(),
            equipe_id=equipe.id,
            criada_por_usuario_id=usuario.id,
            nome=nome_limpo,
            nome_normalizado=nome_normalizado,
            descricao=descricao_limpa or None,
            status=StatusAutomacao.RASCUNHO,
            criada_em=agora,
            atualizada_em=agora,
        )
        return self._automacao_repository.salvar(automacao)
