"""Contrato de cliente HTTP."""

from typing import Any, Protocol


class HttpClientPort(Protocol):
    """Porta para operacoes HTTP de saida."""

    def get_text(self, url: str) -> str | None:
        """Obtem conteudo textual de uma URL."""
        ...

    def get_bytes(self, url: str) -> bytes | None:
        """Obtem conteudo binario de uma URL."""
        ...

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> tuple[int, str, str]:
        """Executa uma requisicao HTTP generica e retorna status, motivo e corpo."""
        ...
