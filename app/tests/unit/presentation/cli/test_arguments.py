"""Testes unitarios para analise de argumentos da CLI."""

import sys

import pytest

from presentation.cli.arguments import parse_args


@pytest.mark.unit
@pytest.mark.interface
def test_parse_args_required(monkeypatch):
    """Testa parse_args com argumentos obrigatorios."""
    monkeypatch.setattr(sys, "argv", ["main.py", "--url", "https://example.com"])
    args = parse_args()
    assert args.url == "https://example.com"
    assert args.skip_download is False
    assert args.no_test is False
    assert args.methods == "get,post"


@pytest.mark.unit
@pytest.mark.interface
def test_parse_args_all(monkeypatch):
    """Testa parse_args com todos os argumentos especificados."""
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
    """Testa parse_args quando --url obrigatorio esta ausente."""
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit):
        parse_args()
