"""Adaptador HTTP sobre urllib (infraestrutura)."""

from __future__ import annotations

import urllib.error
import urllib.request

import structlog

from recon.domain.constants import DEFAULT_BROWSER_HEADERS


class UrllibHttpClient:
    """Implementa `HttpTextClientPort` e `HttpBytesClientPort` com logs estruturados."""

    def __init__(
        self,
        *,
        log: structlog.BoundLogger,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Define logger structlog e cabeçalhos HTTP opcionais."""
        self._log = log
        self._headers = headers or DEFAULT_BROWSER_HEADERS

    def get_text(self, url: str) -> str | None:
        """GET texto."""
        req = urllib.request.Request(url, headers=self._headers)
        try:
            with urllib.request.urlopen(req) as r:
                body = r.read().decode("utf-8", errors="replace")
                self._log.debug("http.get_text.ok", url=url, bytes=len(body.encode("utf-8")))
                return body
        except urllib.error.HTTPError as e:
            self._log.warning("http.get_text.http_error", url=url, status=e.code, reason=e.reason)
            return None
        except urllib.error.URLError as e:
            self._log.warning("http.get_text.url_error", url=url, reason=str(e.reason))
            return None

    def get_bytes(self, url: str) -> bytes | None:
        """GET binário (descarga de assets; falhas menos verbosas)."""
        req = urllib.request.Request(url, headers=self._headers)
        try:
            with urllib.request.urlopen(req) as r:
                data = r.read()
                self._log.debug("http.get_bytes.ok", url=url, bytes=len(data))
                return data
        except urllib.error.HTTPError as e:
            self._log.info("http.get_bytes.skip_http", url=url, status=e.code)
            return None
        except urllib.error.URLError as e:
            self._log.info("http.get_bytes.skip_url", url=url, reason=str(e.reason))
            return None
