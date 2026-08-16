"""Contrato de cliente HTTP."""

from typing import Any, Protocol


class HttpClientPort(Protocol):
    """Port for outbound HTTP operations."""

    def get_text(self, url: str) -> str | None:
        """Fetch text content from a URL."""
        ...

    def get_bytes(self, url: str) -> bytes | None:
        """Fetch binary content from a URL."""
        ...

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> tuple[int, str, str]:
        """Execute a generic HTTP request and return status, reason and body text."""
        ...
