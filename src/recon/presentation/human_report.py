"""Saída legível para terminal (opcional); os dados autoritativos vivem nos logs estruturados."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recon.domain.models import BundleAnalysis


def emit_banner_and_summary(*, banner: str, analysis: BundleAnalysis, app_url: str) -> None:
    """Imprime banner ASCII e tabela-resumo em stderr (modo humano explícito)."""
    print(banner, file=sys.stderr)
    sep = "-" * 52
    base = app_url.rstrip("/")
    print(f"\n{sep}", file=sys.stderr)
    print(f"  App URL        : {base}", file=sys.stderr)
    print(f"  Supabase URL   : {analysis.supabase.base_url}", file=sys.stderr)
    print(f"  anon key       : {analysis.supabase.anon_key[:48]}...", file=sys.stderr)
    print(f"  Auth endpoints : {len(analysis.auth_endpoints)}", file=sys.stderr)
    print(f"  REST Tables    : {len(analysis.tables)}", file=sys.stderr)
    print(f"  RPC calls      : {len(analysis.rpcs)}", file=sys.stderr)
    print(f"  Edge Functions : {len(analysis.edge_functions)}", file=sys.stderr)
    print(sep, file=sys.stderr)
