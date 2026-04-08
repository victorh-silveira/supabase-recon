"""Processador de nível de log em 4 letras."""

from __future__ import annotations

import pytest

from recon.infrastructure.log_level_format import level_to_four_letters


@pytest.mark.parametrize(
    ("incoming", "expected"),
    [
        ("info", "INFO"),
        ("INFO", "INFO"),
        ("warning", "WARN"),
        ("error", "ERRO"),
        ("critical", "CRIT"),
        ("debug", "DBUG"),
        ("notset", "NONE"),
    ],
)
def test_level_to_four_letters_mapping(incoming: str, expected: str) -> None:
    """Níveis conhecidos mapeiam para exatamente 4 caracteres maiúsculos."""
    out = level_to_four_letters(None, "", {"level": incoming, "event": "x"})
    assert out["level"] == expected
    assert len(out["level"]) == 4


def test_level_unknown_truncates_to_four() -> None:
    """Nível desconhecido é truncado/preenchido para 4 caracteres maiúsculos."""
    out = level_to_four_letters(None, "", {"level": "custom", "event": "y"})
    assert out["level"] == "CUST"


def test_level_non_string_keeps_event_dict() -> None:
    """Quando `level` não é string, retorna sem mutação."""
    event = {"level": 10, "event": "z"}
    out = level_to_four_letters(None, "", event)
    assert out is event
    assert out["level"] == 10
