"""Unit tests for HTTPClient."""

import pytest
import requests

from app.infrastructure.network.http_client import HTTPClient


@pytest.fixture
def client():
    """Return an HTTPClient instance."""
    return HTTPClient()


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_text_success(client, monkeypatch):
    """Test successful GET text request."""

    class MockResponse:
        text = "hello world"
        status_code = 200

        def raise_for_status(self):
            pass

    monkeypatch.setattr("requests.Session.get", lambda *args, **kwargs: MockResponse())

    result = client.get_text("https://example.com")
    assert result == "hello world"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_bytes_success(client, monkeypatch):
    """Test successful GET bytes request."""

    class MockResponse:
        content = b"\x00\x01"
        status_code = 200

        def raise_for_status(self):
            pass

    monkeypatch.setattr("requests.Session.get", lambda *args, **kwargs: MockResponse())

    result = client.get_bytes("https://example.com")
    assert result == b"\x00\x01"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_request_exception(client, monkeypatch):
    """Test request handling during an exception."""

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
    """Test successful generic request."""

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
    """Test GET text failing."""

    def mock_get(*args, **kwargs):
        raise requests.RequestException("Error")

    monkeypatch.setattr("requests.Session.get", mock_get)
    assert client.get_text("https://example.com") is None


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_bytes_error(client, monkeypatch):
    """Test GET bytes failing."""

    def mock_get(*args, **kwargs):
        raise requests.RequestException("Error")

    monkeypatch.setattr("requests.Session.get", mock_get)
    assert client.get_bytes("https://example.com") is None


@pytest.mark.unit
@pytest.mark.infrastructure
def test_request_generic_exception(client, monkeypatch):
    """Test request handling during a generic exception."""

    def mock_request(*args, **kwargs):
        raise RuntimeError("Bad")

    monkeypatch.setattr("requests.Session.request", mock_request)

    status, reason, body = client.request("GET", "https://example.com")
    assert status == 0
    assert "Bad" in reason
    assert body == ""
