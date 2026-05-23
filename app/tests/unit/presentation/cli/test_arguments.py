"""Unit tests for CLI argument parsing."""

import sys

import pytest

from src.presentation.cli.arguments import parse_args


@pytest.mark.unit
@pytest.mark.interface
def test_parse_args_required(monkeypatch):
    """Test parse_args with required arguments."""
    monkeypatch.setattr(sys, "argv", ["main.py", "--url", "https://example.com"])
    args = parse_args()
    assert args.url == "https://example.com"
    assert args.skip_download is False
    assert args.no_test is False
    assert args.methods == "get,post"


@pytest.mark.unit
@pytest.mark.interface
def test_parse_args_all(monkeypatch):
    """Test parse_args with all arguments specified."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "--url", "https://example.com", "--skip-download", "--no-test", "--methods", "get,post,put"],
    )
    args = parse_args()
    assert args.url == "https://example.com"
    assert args.skip_download is True
    assert args.no_test is True
    assert args.methods == "get,post,put"


@pytest.mark.unit
@pytest.mark.interface
def test_parse_args_missing_url(monkeypatch):
    """Test parse_args when required --url is missing."""
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit):
        parse_args()
