"""Testes unitarios para o adaptador HTTPClient."""

import pytest
import requests

from infrastructure.adapters.http_client import HTTPClient


@pytest.fixture
def client():
    """Retorna uma instancia de HTTPClient."""
    return HTTPClient()


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_text_success(client, monkeypatch):
    """Testa requisicao GET de texto bem-sucedida."""

    class MockResponse:
        text = "hello world"
        status_code = 200

        def raise_for_status(self):
            return None

    monkeypatch.setattr("requests.Session.get", lambda *args, **kwargs: MockResponse())

    result = client.get_text("https://example.com")
    assert result == "hello world"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_bytes_success(client, monkeypatch):
    """Testa requisicao GET de bytes bem-sucedida."""

    class MockResponse:
        content = b"\x00\x01"
        status_code = 200

        def raise_for_status(self):
            return None

    monkeypatch.setattr("requests.Session.get", lambda *args, **kwargs: MockResponse())

    result = client.get_bytes("https://example.com")
    assert result == b"\x00\x01"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_request_exception(client, monkeypatch):
    """Testa tratamento de requisicao durante uma excecao."""

    def mock_request(*args, **kwargs):
        raise requests.RequestException("Boom")

    monkeypatch.setattr("requests.Session.request", mock_request)

    status, reason, body = client.request("GET", "https://example.com")
    assert status == 0
    assert "Boom" in reason
    assert body == ""


@pytest.mark.unit
@pytest.mark.infrastructure
def test_request_success(client, monkeypatch):
    """Testa requisicao generica bem-sucedida."""

    class MockResponse:
        status_code = 201
        reason = "Created"
        text = "done"

    monkeypatch.setattr("requests.Session.request", lambda *args, **kwargs: MockResponse())

    status, reason, body = client.request("POST", "https://example.com")
    assert status == 201
    assert reason == "Created"
    assert body == "done"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_text_error(client, monkeypatch):
    """Testa falha em GET de texto."""

    def mock_get(*args, **kwargs):
        raise requests.RequestException("Error")

    monkeypatch.setattr("requests.Session.get", mock_get)
    assert client.get_text("https://example.com") is None


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_bytes_error(client, monkeypatch):
    """Testa falha em GET de bytes."""

    def mock_get(*args, **kwargs):
        raise requests.RequestException("Error")

    monkeypatch.setattr("requests.Session.get", mock_get)
    assert client.get_bytes("https://example.com") is None


@pytest.mark.unit
@pytest.mark.infrastructure
def test_request_generic_exception(client, monkeypatch):
    """Testa tratamento de requisicao durante uma excecao generica."""

    def mock_request(*args, **kwargs):
        raise RuntimeError("Bad")

    monkeypatch.setattr("requests.Session.request", mock_request)

    status, reason, body = client.request("GET", "https://example.com")
    assert status == 0
    assert "Bad" in reason
    assert body == ""
