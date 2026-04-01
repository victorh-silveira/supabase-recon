"""Agregação pura dos resultados de sonda HTTP."""

from __future__ import annotations

from recon.domain.constants import ACCESSIBLE_HTTP_STATUSES
from recon.domain.models import ProbeSummary, SingleProbeResult


def aggregate_probe_results(results: list[SingleProbeResult]) -> ProbeSummary:
    """Classifica resultados de sonda por faixa HTTP."""
    accessible: list[SingleProbeResult] = []
    requires_auth: list[SingleProbeResult] = []
    not_found: list[SingleProbeResult] = []
    error_or_offline: list[SingleProbeResult] = []

    for r in results:
        if r.status_code in ACCESSIBLE_HTTP_STATUSES:
            accessible.append(r)
        elif r.status_code in (401, 403):
            requires_auth.append(r)
        elif r.status_code == 404:
            not_found.append(r)
        else:
            error_or_offline.append(r)

    return ProbeSummary(
        accessible=accessible,
        requires_auth=requires_auth,
        not_found=not_found,
        error_or_offline=error_or_offline,
    )
