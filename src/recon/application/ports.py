"""Contratos invertidos (Clean Architecture)."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from recon.domain.models import ProbeSummary


@runtime_checkable
class HttpTextClientPort(Protocol):
    """Cliente HTTP que devolve texto UTF-8 ou None se falhar."""

    def get_text(self, url: str) -> str | None:
        """GET; devolve corpo como string ou None."""


@runtime_checkable
class HttpBytesClientPort(Protocol):
    """Cliente HTTP que devolve bytes brutos."""

    def get_bytes(self, url: str) -> bytes | None:
        """GET; devolve corpo binário ou None."""


@runtime_checkable
class JsonObjectWriterPort(Protocol):
    """Escreve um objeto serializável (ex.: dict OpenAPI) como ficheiro."""

    def write_yaml(self, path: Path, document: dict) -> None:
        """Serializa `document` em YAML no caminho dado."""


@runtime_checkable
class EndpointProbePort(Protocol):
    """Executa sondas HTTP contra paths do OpenAPI gerado."""

    def run_probes(self, swagger: dict, anon_key: str, methods: frozenset[str]) -> ProbeSummary:
        """Devolve agregação `ProbeSummary`."""
