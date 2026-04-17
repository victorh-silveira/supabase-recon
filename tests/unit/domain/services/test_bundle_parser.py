"""Unit tests for BundleParserService."""

import pytest

from app.domain.exceptions import SupabaseConfigNotFoundError
from app.domain.services.bundle_parser import BundleParserService


@pytest.fixture
def parser():
    """Return a BundleParserService instance."""
    return BundleParserService()


@pytest.mark.unit
@pytest.mark.domain
def test_discover_config_success(parser):
    """Test successful discovery of Supabase config."""
    content = 'url: "https://project.supabase.co", key: "eyJabc.123.xyz"'  # gitleaks:allow
    config = parser.discover_config(content)
    assert config.url == "https://project.supabase.co"
    assert config.anon_key == "eyJabc.123.xyz"  # gitleaks:allow


@pytest.mark.unit
@pytest.mark.domain
def test_discover_config_not_found(parser):
    """Test failure when anonKey is missing."""
    content = "nothing here"
    with pytest.raises(SupabaseConfigNotFoundError):
        parser.discover_config(content)


@pytest.mark.unit
@pytest.mark.domain
def test_extract_rest_tables(parser):
    """Test extraction of REST tables."""
    content = '.from("profiles").from("posts")'
    endpoints = parser.extract_rest_tables(content)
    # 2 tables * 4 methods each = 8 endpoints
    assert len(endpoints) == 8


@pytest.mark.unit
@pytest.mark.domain
def test_extract_auth_endpoints(parser):
    """Test extraction of Auth endpoints from Mr calls."""
    content = """
    Mr(this.fetch, "POST", `${this.url}/auth/v1/signup`, {body: {email: e, password: p}});
    """
    endpoints = parser.extract_auth_endpoints(content)
    assert len(endpoints) == 1
    ep = endpoints[0]
    assert ep.method == "POST"
    assert "/auth/v1/signup" in ep.path
    assert "email" in ep.body_keys
    assert "password" in ep.body_keys


@pytest.mark.unit
@pytest.mark.domain
def test_extract_auth_endpoints_duplicate(parser):
    """Test deduplication of Auth endpoints."""
    content = """
    Mr(this.fetch, "POST", `${this.url}/auth/v1/signup`, {body: {email: e}});
    Mr(this.fetch, "POST", `${this.url}/auth/v1/signup`, {body: {email: e}});
    """
    endpoints = parser.extract_auth_endpoints(content)
    assert len(endpoints) == 1


@pytest.mark.unit
@pytest.mark.domain
def test_extract_rpc_calls(parser):
    """Test extraction of RPC calls."""
    content = '.rpc("get_user_profile")'
    endpoints = parser.extract_rpc_calls(content)
    assert len(endpoints) == 1
    assert endpoints[0].method == "POST"
    assert "rpc/get_user_profile" in endpoints[0].path


@pytest.mark.unit
@pytest.mark.domain
def test_extract_edge_functions(parser):
    """Test extraction of Edge Functions."""
    content = "https://abc.supabase.co/functions/v1/heavy-task"
    endpoints = parser.extract_edge_functions(content)
    assert len(endpoints) == 1
    assert "functions/v1/heavy-task" in endpoints[0].path


@pytest.mark.unit
@pytest.mark.domain
def test_path_helpers(parser):
    """Test private path parsing helpers."""
    assert parser._js_path_to_openapi("${this.id}") == "{id}"
    assert parser._extract_path_params("/{id}/info/{name}") == ["id", "name"]

    qparams = parser._extract_static_query("/path?a=1&b=2")
    assert len(qparams) == 2
    assert qparams[0].key == "a"
    assert qparams[0].value == "1"
