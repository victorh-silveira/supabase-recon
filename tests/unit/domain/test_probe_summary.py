"""Testes da agregação de resultados de sonda."""

from __future__ import annotations

from recon.domain.models import SingleProbeResult
from recon.domain.probe_summary import aggregate_probe_results


def _one(path: str, method: str, status: int) -> SingleProbeResult:
    return SingleProbeResult(
        method=method,
        path=path,
        url=f"https://x{path}",
        status_code=status,
        reason="",
        body_preview="",
        tag="t",
    )


def test_aggregate_probe_results_buckets() -> None:
    """Classifica 200 / 401 / 404 / erro em listas distintas."""
    results = [
        _one("/a", "get", 200),
        _one("/b", "get", 401),
        _one("/c", "get", 404),
        _one("/d", "get", 0),
    ]
    summary = aggregate_probe_results(results)
    assert len(summary.accessible) == 1
    assert len(summary.requires_auth) == 1
    assert len(summary.not_found) == 1
    assert len(summary.error_or_offline) == 1
