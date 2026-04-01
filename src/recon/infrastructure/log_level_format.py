"""Códigos de nível de log fixos em 4 letras MAIÚSCULAS (structlog)."""

from __future__ import annotations

import structlog.typing

# Mapeamento explícito: nível padrão structlog/logging → 4 letras
_LEVEL_CODES: dict[str, str] = {
    "notset": "NONE",
    "debug": "DBUG",
    "info": "INFO",
    "warning": "WARN",
    "error": "ERRO",
    "critical": "CRIT",
}


def level_to_four_letters(
    _logger: object,
    _method_name: str,
    event_dict: structlog.typing.EventDict,
) -> structlog.typing.EventDict:
    """Substitui `level` por código de 4 letras maiúsculas (p.ex. INFO, WARN, ERRO)."""
    raw = event_dict.get("level")
    if not isinstance(raw, str):
        return event_dict
    key = raw.lower().strip()
    code = _LEVEL_CODES.get(key)
    if code is None:
        code = (key + "    ")[:4].upper()
    event_dict["level"] = code
    return event_dict
