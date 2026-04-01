"""Sink humano opcional."""

from __future__ import annotations

from recon.domain.models import BundleAnalysis, SupabaseProjectConfig
from recon.presentation.human_report import emit_human_summary


def test_emit_human_summary_writes_stderr(capsys) -> None:
    """Função imprime linhas de resumo em stderr."""
    analysis = BundleAnalysis(
        supabase=SupabaseProjectConfig(base_url="https://p.co", anon_key="eyJx.y.z"),
        auth_endpoints=[],
        tables=["a"],
        rpcs=["r"],
        edge_functions=["e"],
    )
    emit_human_summary(analysis=analysis, app_url="https://app/")
    err = capsys.readouterr().err
    assert "Supabase URL" in err
    assert "REST Tables" in err
    assert "RPC calls" in err
    assert "Edge Functions" in err
