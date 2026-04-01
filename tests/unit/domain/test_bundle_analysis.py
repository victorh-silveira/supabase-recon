"""Testes do módulo de análise estática do bundle."""

from __future__ import annotations

import pytest

from recon.domain.bundle_analysis import (
    analyze_bundle_content,
    discover_supabase_config,
    extract_auth_endpoints,
    extract_edge_functions,
    extract_rpc,
    extract_tables,
    js_path_to_openapi,
    normalize_app_base_url,
    path_params,
    static_query,
)
from recon.domain.exceptions import MissingAnonKeyError


def test_normalize_app_base_url_strips_trailing_slash() -> None:
    """URL base não deve terminar em slash."""
    assert normalize_app_base_url("https://x.com/") == "https://x.com"


def test_normalize_app_base_url_upgrades_http_to_https() -> None:
    """http:// deve tornar-se https:// (evita bloqueio de porta 80 / redirect)."""
    assert normalize_app_base_url("http://seuagentetrader.com/") == "https://seuagentetrader.com"


def test_js_path_to_openapi_trims_placeholder_tail() -> None:
    """${ns.id} deve virar {id}."""
    assert js_path_to_openapi("/users/${user.id}/x") == "/users/{id}/x"


def test_path_params_finds_names() -> None:
    """Detecta placeholders OpenAPI no path."""
    assert path_params("/a/{id}/b/{x}") == ["id", "x"]


def test_static_query_parses_pairs() -> None:
    """Query string estática vira lista de dicts."""
    assert static_query("/p?a=1&b=two") == [
        {"key": "a", "value": "1"},
        {"key": "b", "value": "two"},
    ]


def test_static_query_without_query() -> None:
    """Path sem ? devolve lista vazia."""
    assert static_query("/only/path") == []


def test_discover_supabase_config_success(fake_jwt: str) -> None:
    """Com URL e JWT presentes devolve config."""
    content = f' "{fake_jwt}" "https://abc.supabase.co" '
    cfg = discover_supabase_config(content)
    assert cfg.base_url == "https://abc.supabase.co"
    assert cfg.anon_key == fake_jwt


def test_discover_supabase_config_missing_anon_raises() -> None:
    """Sem anon key válido levanta erro de domínio."""
    with pytest.raises(MissingAnonKeyError):
        discover_supabase_config('"https://z.supabase.co" and no token here')


def test_extract_tables_sorts_unique() -> None:
    """Tabelas extraídas são únicas e ordenadas."""
    js = '.from("b").from("a").from("b")'
    assert extract_tables(js) == ["a", "b"]


def test_extract_rpc_sorts_unique() -> None:
    """RPCs extraídos são únicos e ordenados."""
    js = '.rpc("z").rpc("a").rpc("a")'
    assert extract_rpc(js) == ["a", "z"]


def test_extract_edge_functions() -> None:
    """Slugs de edge aparecem no conjunto."""
    js = "x supabase.co/functions/v1/alpha y supabase.co/functions/v1/beta"
    assert extract_edge_functions(js) == ["alpha", "beta"]


def test_extract_auth_endpoints_minimal_snippet() -> None:
    """Snippet Mr(fetch, GET, ...) gera AuthEndpoint."""
    js = 'Mr(this.fetch, "GET", `${this.url}/admin/users?x=1`, {} )'
    eps = extract_auth_endpoints(js)
    assert len(eps) == 1
    assert eps[0].method == "GET"
    assert "/admin/users" in eps[0].path
    assert eps[0].query_params == [{"key": "x", "value": "1"}]


def test_analyze_bundle_content_integrates(minimal_bundle_js: str, fake_jwt: str) -> None:
    """Pipeline completo de análise sobre fragmento mínimo."""
    analysis = analyze_bundle_content(minimal_bundle_js)
    assert analysis.supabase.base_url == "https://projunit.supabase.co"
    assert analysis.supabase.anon_key == fake_jwt
    assert "users" in analysis.tables
    assert "count_rows" in analysis.rpcs
    assert "hello_edge" in analysis.edge_functions
