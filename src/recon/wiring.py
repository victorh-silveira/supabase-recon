"""Raiz de composição: instancia adaptadores de infra e o orquestrador."""

from __future__ import annotations

import structlog

from recon.application.recon_orchestrator import ReconOrchestrator
from recon.infrastructure.http_urllib import UrllibHttpClient
from recon.infrastructure.probe_client import UrllibEndpointProbe
from recon.infrastructure.yaml_writer import PyyamlOpenAPIWriter


def build_orchestrator(log: structlog.BoundLogger | None = None) -> ReconOrchestrator:
    """Monta o grafo padrão (urllib + YAML + sondagem)."""
    logger = log or structlog.get_logger()
    http = UrllibHttpClient(log=logger)
    return ReconOrchestrator(
        http_text=http,
        http_bytes=http,
        spec_writer=PyyamlOpenAPIWriter(),
        endpoint_probe=UrllibEndpointProbe(log=logger),
        log=logger,
    )
