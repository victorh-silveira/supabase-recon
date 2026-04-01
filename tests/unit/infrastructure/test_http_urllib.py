"""Cliente HTTP urllib com urlopen mockado."""

from __future__ import annotations

import urllib.error
from unittest.mock import patch

import structlog

from recon.infrastructure.http_urllib import UrllibHttpClient


def test_get_text_success() -> None:
    """get_text devolve string UTF-8."""
    log = structlog.get_logger()
    client = UrllibHttpClient(log=log)
    with patch("recon.infrastructure.http_urllib.urllib.request.urlopen") as m:
        m.return_value.__enter__.return_value.read.return_value = b"\xc3\xa1"  # á
        assert client.get_text("https://example.test/x") == "á"
        m.assert_called_once()


def test_get_text_http_error_returns_none() -> None:
    """HTTPError resulta em None."""
    log = structlog.get_logger()
    client = UrllibHttpClient(log=log)
    with patch("recon.infrastructure.http_urllib.urllib.request.urlopen") as m:
        m.side_effect = urllib.error.HTTPError("https://example.test/missing", 404, "nf", {}, None)
        assert client.get_text("https://example.test/missing") is None


def test_get_bytes_success() -> None:
    """get_bytes devolve bytes brutos."""
    log = structlog.get_logger()
    client = UrllibHttpClient(log=log)
    with patch("recon.infrastructure.http_urllib.urllib.request.urlopen") as m:
        m.return_value.__enter__.return_value.read.return_value = b"\x00\xff"
        assert client.get_bytes("https://example.test/bin") == b"\x00\xff"
