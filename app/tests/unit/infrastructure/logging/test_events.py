"""Unit tests for semantic logging helpers."""

import logging

import pytest

from infrastructure.logging.events import log_event, redact_url


@pytest.mark.unit
@pytest.mark.infrastructure
def test_redact_url_with_query():
    """Query string must be redacted."""
    assert redact_url("https://h.example/path?token=secret") == "https://h.example/path?***"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_redact_url_without_query():
    """URL without query stays unchanged."""
    assert redact_url("https://h.example/path") == "https://h.example/path"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_log_event_redacts_secrets(caplog):
    """Sensitive fields are masked in the log message."""
    logger = logging.getLogger("test.events")
    with caplog.at_level(logging.INFO, logger="test.events"):
        log_event(
            logger,
            logging.INFO,
            "recon.test.event",
            url="https://h.example/x?a=1",
            anon_key="super-secret",
            count=1,
        )
    assert "event=recon.test.event" in caplog.text
    assert "url=https://h.example/x?***" in caplog.text
    assert "anon_key=***" in caplog.text
    assert "super-secret" not in caplog.text
