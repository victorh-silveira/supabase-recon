"""Modelos e DTOs imutáveis do domínio."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AuthEndpoint:
    """Endpoint Auth Admin/GoTrue inferido do bundle."""

    method: str
    path: str
    path_params: list[str]
    query_params: list[dict[str, str]]
    body_keys: list[str]


@dataclass(frozen=True, slots=True)
class SupabaseProjectConfig:
    """URL do projeto e chave anónima descobertas no JS."""

    base_url: str
    anon_key: str


@dataclass(frozen=True, slots=True)
class BundleAnalysis:
    """Resultado da análise estática do bundle principal."""

    supabase: SupabaseProjectConfig
    auth_endpoints: list[AuthEndpoint]
    tables: list[str]
    rpcs: list[str]
    edge_functions: list[str]


@dataclass(frozen=True, slots=True)
class SingleProbeResult:
    """Uma chamada de sonda a um path/método."""

    method: str
    path: str
    url: str
    status_code: int
    reason: str
    body_preview: str
    tag: str


@dataclass(frozen=True, slots=True)
class ProbeSummary:
    """Agregação DRY das sondas (domínio puro)."""

    accessible: list[SingleProbeResult] = field(default_factory=list)
    requires_auth: list[SingleProbeResult] = field(default_factory=list)
    not_found: list[SingleProbeResult] = field(default_factory=list)
    error_or_offline: list[SingleProbeResult] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ReconPaths:
    """Caminhos de saída derivados da URL da app."""

    output_dir: Path
    swagger_file: Path
