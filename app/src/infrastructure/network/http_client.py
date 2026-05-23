"""HTTP client implementation using requests."""

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class HTTPClient:
    """Robust HTTP client for downloading assets and testing endpoints."""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
    }

    def __init__(self, timeout: int = 10, retries: int = 3):
        """Initialize the client with timeout and retry policy."""
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
        """Fetch text content from a URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"HTTP GET Error: {e} | URL: {url}")
            return None

    def get_bytes(self, url: str) -> bytes | None:
        """Fetch binary content from a URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.warning(f"HTTP GET (bytes) skip: {e} | URL: {url}")
            return None

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> tuple[int, str, str]:
        """Execute a generic HTTP request and return (status, reason, response_text)."""
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json_data,
                timeout=self.timeout,
            )
            return response.status_code, response.reason, response.text
        except Exception as e:  # noqa: BLE001
            logger.error(f"Unexpected request error: {e}")
            return 0, str(e), ""
