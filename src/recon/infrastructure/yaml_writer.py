"""Serialização OpenAPI → ficheiro YAML."""

from __future__ import annotations

from pathlib import Path

import yaml


class PyyamlOpenAPIWriter:
    """Escreve dict OpenAPI como YAML com Unicode preservado."""

    def write_yaml(self, path: Path, document: dict) -> None:
        """Grava `document` em `path` (UTF-8)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        text = yaml.dump(document, allow_unicode=True, sort_keys=False)
        path.write_text(text, encoding="utf-8")
