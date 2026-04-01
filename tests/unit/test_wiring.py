"""Composição padrão do orquestrador."""

from __future__ import annotations

from unittest.mock import MagicMock

from recon.application.recon_orchestrator import ReconOrchestrator
from recon.wiring import build_orchestrator


def test_build_orchestrator_returns_configured_instance() -> None:
    """Grafo default é ReconOrchestrator com dependências reais."""
    log = MagicMock()
    orch = build_orchestrator(log=log)
    assert isinstance(orch, ReconOrchestrator)
