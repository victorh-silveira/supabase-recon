"""Integration tests for HTTPClient with mock transport."""

from __future__ import annotations

from typing import Any

import pytest
from requests import Response
from requests.adapters import BaseAdapter

from infrastructure.adapters.http_client import HTTPClient


class MockTransport(BaseAdapter):
    """In-memory transport that returns canned HTTP responses."""

    def __init__(self, status: int = 200, body: str = "ok") -> None:
        """Store canned response attributes."""
        super().__init__()
        self.status = status
        self.body = body
        self.calls: list[str] = []

    def send(self, request: Any, **kwargs: Any) -> Response:
        """Return a synthetic Response."""
        self.calls.append(request.url)
        response = Response()
        response.status_code = self.status
        response._content = self.body.encode("utf-8")
        response.url = request.url
        response.reason = "OK" if self.status < 400 else "Error"
        response.request = request
        return response

    def close(self) -> None:
        """No-op close for adapter protocol."""
        return


@pytest.mark.integration
@pytest.mark.infrastructure
def test_http_client_get_text_via_mock_transport():
    """HTTPClient get_text works against a mounted mock transport."""
    client = HTTPClient(timeout=5, retries=0)
    transport = MockTransport(status=200, body="hello-integration")
    client.session.mount("https://", transport)

    result = client.get_text("https://example.test/page")
    assert result == "hello-integration"
    assert transport.calls


@pytest.mark.integration
@pytest.mark.infrastructure
def test_http_client_request_via_mock_transport():
    """HTTPClient request returns status and body from mock transport."""
    client = HTTPClient(timeout=5, retries=0)
    transport = MockTransport(status=201, body='{"id":1}')
    client.session.mount("https://", transport)

    status, reason, body = client.request("POST", "https://example.test/items", json_data={"a": 1})
    assert status == 201
    assert body == '{"id":1}'
