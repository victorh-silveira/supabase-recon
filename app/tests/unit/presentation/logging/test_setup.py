"""Unit tests for presentation logging setup."""

import logging

import pytest

from presentation.logging.setup import configure_logging


@pytest.mark.unit
@pytest.mark.presentation
def test_configure_logging():
    """configure_logging sets root level and quiets HTTP loggers."""
    configure_logging("WARNING")
    assert logging.getLogger().level == logging.WARNING
    assert logging.getLogger("urllib3").level == logging.WARNING
    assert logging.getLogger("requests").level == logging.WARNING
