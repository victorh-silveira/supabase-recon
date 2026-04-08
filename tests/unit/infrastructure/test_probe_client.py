"""Testes do cliente de sondagem urllib."""

from __future__ import annotations

import io
import urllib.error
from unittest.mock import MagicMock, patch

import structlog

from recon.infrastructure.probe_client import (
    UrllibEndpointProbe,
    UrllibProbeTransport,
    _fill_path,
    _pretty_body,
)


class _Resp:
    def __init__(self, *, status: int, body: str) -> None:
        self.status = status
        self._body = body.encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        _ = (exc_type, exc, tb)
        return False


def test_fill_path_replaces_known_and_unknown_params() -> None:
    """Substitui placeholders conhecidos e gera fallback para os desconhecidos."""
    assert _fill_path("/rest/v1/t/{id}/{custom}") == "/rest/v1/t/00000000-0000-0000-0000-000000000000/test-custom"


def test_pretty_body_json_and_truncation() -> None:
    """Formata JSON e trunca payloads longos com sufixo padrão."""
    assert '"a": 1' in _pretty_body('{"a":1}')
    long_raw = "x" * 700
    assert _pretty_body(long_raw).endswith("... (truncated)")


def test_transport_request_success_and_http_error() -> None:
    """Transport devolve sucesso em 200 e mapeia HTTPError com body."""
    tr = UrllibProbeTransport(anon_key="k", log=structlog.get_logger())
    with patch("recon.infrastructure.probe_client.urllib.request.urlopen") as m:
        m.return_value = _Resp(status=200, body='{"ok":true}')
        status, reason, body = tr.request("get", "https://x")
        assert (status, reason) == (200, "")
        assert '"ok"' in body

        m.side_effect = urllib.error.HTTPError("https://x", 401, "unauth", {}, io.BytesIO(b'{"e":"x"}'))
        status, reason, body = tr.request("post", "https://x")
        assert status == 401
        assert reason == "unauth"
        assert '"e"' in body


def test_transport_request_url_and_os_error() -> None:
    """URLError e OSError devem retornar status 0 sem levantar exceção."""
    log = MagicMock()
    tr = UrllibProbeTransport(anon_key="k", log=log)
    with patch("recon.infrastructure.probe_client.urllib.request.urlopen") as m:
        m.side_effect = urllib.error.URLError("offline")
        assert tr.request("get", "https://x")[0] == 0
        m.side_effect = OSError("boom")
        assert tr.request("get", "https://x")[0] == 0


def test_endpoint_probe_non_dict_paths_returns_empty_summary() -> None:
    """Quando `paths` não é dict, o resumo agregado deve ser vazio."""
    probe = UrllibEndpointProbe(log=MagicMock())
    summary = probe.run_probes({"servers": [{"url": "https://x"}], "paths": []}, "k", frozenset({"get"}))
    assert summary.accessible == []


def test_endpoint_probe_filters_methods_and_collects_results() -> None:
    """Executa somente métodos permitidos e coleta resultados acessíveis."""
    log = MagicMock()
    probe = UrllibEndpointProbe(log=log)
    swagger = {
        "servers": [{"url": "https://proj.supabase.co"}],
        "paths": {
            "/rest/v1/users/{id}": {
                "get": {"tags": ["rest"]},
                "post": {"tags": ["rest"]},
            },
            "/bad": "not-a-dict",
            "/rpc": {"get": "not-a-dict"},
        },
    }
    with patch.object(UrllibProbeTransport, "request", return_value=(200, "", '{"ok":true}')):
        summary = probe.run_probes(swagger, "k", frozenset({"get"}))
    assert len(summary.accessible) == 1
    assert summary.accessible[0].method == "GET"


def test_status_icon_fallback() -> None:
    """Status desconhecido usa ícone padrão de erro."""
    assert UrllibEndpointProbe._status_icon(999) == "[ERR] "
