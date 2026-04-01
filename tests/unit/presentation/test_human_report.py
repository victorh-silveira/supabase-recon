"""Sink humano opcional."""

from __future__ import annotations

from recon.domain.models import BundleAnalysis, SupabaseProjectConfig
from recon.presentation.human_report import emit_banner_and_summary


def test_emit_banner_and_summary_writes_stderr(capsys) -> None:
    """Função imprime banner e linhas de resumo em stderr."""
    analysis = BundleAnalysis(
        supabase=SupabaseProjectConfig(base_url="https://p.co", anon_key="eyJx.y.z"),
        auth_endpoints=[],
        tables=["a"],
        rpcs=["r"],
        edge_functions=["e"],
    )
    emit_banner_and_summary(banner="BAN\nNER\n", analysis=analysis, app_url="https://app/")
    err = capsys.readouterr().err
    assert "BAN" in err
    assert "Supabase URL" in err
    assert "REST Tables" in err
    assert "RPC calls" in err
    assert "Edge Functions" in err
