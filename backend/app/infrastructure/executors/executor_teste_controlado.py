from dataclasses import dataclass
import subprocess
import sys
from threading import Lock
from uuid import UUID

from app.application.services.executor_automacao import (
    ExecucaoCanceladaError,
    ExecutorAutomacao,
    FalhaControladaAutomacaoError,
    MENSAGEM_FALHA_CONTROLADA,
)
from app.domain.entities.automacao import Automacao
from app.domain.enums.tipo_acao_automacao import TipoAcaoAutomacao


CODIGO_FALHA_CONTROLADA = 2
DURACAO_PADRAO_SEGUNDOS = 60.0
TEMPO_LIMITE_ENCERRAMENTO_SEGUNDOS = 5.0


@dataclass(slots=True)
class _ControleProcesso:
    cancelamento_solicitado: bool = False
    processo: subprocess.Popen[bytes] | None = None


class ExecutorTesteControlado(ExecutorAutomacao):
    """Executa cada cenário controlado em um subprocesso independente."""

    def __init__(
        self,
        duracao_segundos: float = DURACAO_PADRAO_SEGUNDOS,
    ) -> None:
        self._duracao_segundos = duracao_segundos
        self._controles: dict[UUID, _ControleProcesso] = {}
        self._lock = Lock()

    def preparar(self, execucao_id: UUID) -> None:
        with self._lock:
            if execucao_id in self._controles:
                raise RuntimeError("A execução já foi preparada.")
            self._controles[execucao_id] = _ControleProcesso()

    def executar(self, execucao_id: UUID, automacao: Automacao) -> None:
        if automacao.tipo_acao is not TipoAcaoAutomacao.TESTE_CONTROLADO:
            raise ValueError("Tipo de ação não suportado pelo executor.")

        with self._lock:
            controle = self._controles.get(execucao_id)
            if controle is None:
                raise RuntimeError("A execução não foi preparada.")
            if controle.cancelamento_solicitado:
                raise ExecucaoCanceladaError

        processo = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "app.infrastructure.executors.script_teste_controlado",
                "--duracao-segundos",
                str(self._duracao_segundos),
                "--resultado",
                automacao.configuracao_acao.resultado.value,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with self._lock:
            controle = self._controles.get(execucao_id)
            if controle is None:
                self._encerrar_processo(processo)
                raise ExecucaoCanceladaError
            controle.processo = processo
            cancelamento_solicitado = controle.cancelamento_solicitado

        if cancelamento_solicitado:
            self._encerrar_processo(processo)

        codigo_retorno = processo.wait()

        with self._lock:
            controle = self._controles.get(execucao_id)
            if controle is None or controle.cancelamento_solicitado:
                raise ExecucaoCanceladaError

        if codigo_retorno == CODIGO_FALHA_CONTROLADA:
            raise FalhaControladaAutomacaoError(MENSAGEM_FALHA_CONTROLADA)
        if codigo_retorno != 0:
            raise RuntimeError(
                "O processo controlado terminou com código inesperado."
            )

    def cancelar(self, execucao_id: UUID) -> bool:
        with self._lock:
            controle = self._controles.get(execucao_id)
            if controle is None:
                return False
            controle.cancelamento_solicitado = True
            processo = controle.processo

        if processo is not None and processo.poll() is None:
            self._encerrar_processo(processo)
        return True

    def liberar(self, execucao_id: UUID) -> None:
        with self._lock:
            self._controles.pop(execucao_id, None)

    def encerrar_todos(self) -> None:
        with self._lock:
            processos = [
                controle.processo
                for controle in self._controles.values()
                if controle.processo is not None
            ]

        for processo in processos:
            if processo.poll() is None:
                self._encerrar_processo(processo)

    @staticmethod
    def _encerrar_processo(processo: subprocess.Popen[bytes]) -> None:
        processo.terminate()
        try:
            processo.wait(timeout=TEMPO_LIMITE_ENCERRAMENTO_SEGUNDOS)
        except subprocess.TimeoutExpired:
            processo.kill()
            processo.wait()
