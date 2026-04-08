"""Testes da fábrica OpenAPI."""

from __future__ import annotations

from recon.domain.models import AuthEndpoint
from recon.domain.swagger_factory import build_openapi_spec


def test_build_openapi_spec_contains_paths_and_servers() -> None:
    """Documento tem openapi, servers, paths e info."""
    spec = build_openapi_spec(
        [],
        ["items"],
        ["do_ping"],
        ["fn1"],
        "https://ref.supabase.co",
        "eyJh.b.c",
        "https://app.example",
    )
    assert spec["openapi"] == "3.0.3"
    assert spec["servers"][0]["url"] == "https://ref.supabase.co"
    assert "/rest/v1/items" in spec["paths"]
    assert "/rest/v1/rpc/do_ping" in spec["paths"]
    assert "/functions/v1/fn1" in spec["paths"]


def test_build_openapi_spec_auth_endpoint_creates_auth_v1_path() -> None:
    """AuthEndpoint vira operação sob /auth/v1."""
    ep = AuthEndpoint(
        method="POST",
        path="/otp",
        path_params=[],
        query_params=[],
        body_keys=["email"],
    )
    spec = build_openapi_spec(
        [ep],
        [],
        [],
        [],
        "https://p.supabase.co",
        "anonkey",
        "https://app",
    )
    assert "/auth/v1/otp" in spec["paths"]
    assert "post" in spec["paths"]["/auth/v1/otp"]


def test_build_openapi_spec_auth_query_params_become_openapi_parameters() -> None:
    """Query params de AuthEndpoint entram como parâmetros OpenAPI."""
    ep = AuthEndpoint(
        method="GET",
        path="/admin/users",
        path_params=[],
        query_params=[{"key": "page", "value": "1"}],
        body_keys=[],
    )
    spec = build_openapi_spec(
        [ep],
        [],
        [],
        [],
        "https://p.supabase.co",
        "anonkey",
        "https://app",
    )
    params = spec["paths"]["/auth/v1/admin/users"]["get"]["parameters"]
    assert any(p["in"] == "query" and p["name"] == "page" for p in params)
