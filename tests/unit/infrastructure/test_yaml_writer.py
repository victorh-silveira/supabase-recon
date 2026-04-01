"""Serialização YAML do OpenAPI."""

from __future__ import annotations

from pathlib import Path

import yaml

from recon.infrastructure.yaml_writer import PyyamlOpenAPIWriter


def test_pyyaml_openapi_writer_roundtrip(tmp_path: Path) -> None:
    """Grava dict e volta a ler com PyYAML."""
    writer = PyyamlOpenAPIWriter()
    path = tmp_path / "spec.yaml"
    doc = {"openapi": "3.0.3", "info": {"title": "T", "version": "1"}, "paths": {}}
    writer.write_yaml(path, doc)
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert loaded["openapi"] == "3.0.3"
    assert loaded["info"]["title"] == "T"
