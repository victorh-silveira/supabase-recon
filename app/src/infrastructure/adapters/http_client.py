"""Adaptador de cliente HTTP utilizando requests."""

from __future__ import annotations

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from infrastructure.logging.events import log_event


logger = logging.getLogger(__name__)


class HTTPClient:
    """Cliente HTTP robusto para download de assets e teste de endpoints."""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
    }

    def __init__(self, timeout: int = 10, retries: int = 3) -> None:
        """Inicializa o cliente com timeout e politica de retentativas."""
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get_text(self, url: str) -> str | None:
        """Obtem conteudo textual de uma URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            log_event(logger, logging.ERROR, "recon.http.get_text.failed", url=url)
            return None

    def get_bytes(self, url: str) -> bytes | None:
        """Obtem conteudo binario de uma URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException:
            log_event(logger, logging.WARNING, "recon.http.get_bytes.skipped", url=url)
            return None

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> tuple[int, str, str]:
        """Executa uma requisicao HTTP generica e retorna (status, motivo, corpo_texto)."""
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            )
            return response.status_code, response.reason, response.text
        except Exception as e:
            log_event(
                logger,
                logging.ERROR,
                "recon.http.request.failed",
                url=url,
                method=method.upper(),
                error=str(e),
                exc_info=True,
            )
            return 0, str(e), ""
