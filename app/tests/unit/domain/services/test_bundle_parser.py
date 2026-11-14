"""Testes unitarios para BundleParserService."""

import pytest

from domain.exceptions import SupabaseConfigNotFoundError
from domain.services.bundle_parser import BundleParserService


@pytest.fixture
def parser():
    """Retorna uma instancia de BundleParserService."""
    return BundleParserService()


@pytest.mark.unit
@pytest.mark.domain
def test_discover_config_success(parser):
    """Testa descoberta bem-sucedida da configuracao do Supabase."""
    content = 'url: "https://project.supabase.co", key: "eyJabc.123.xyz"'
    config = parser.discover_config(content)
    assert config.url == "https://project.supabase.co"
    assert config.anon_key == "eyJabc.123.xyz"


@pytest.mark.unit
@pytest.mark.domain
def test_discover_config_adjacent_url_and_key(parser):
    """Primeiro regex de JWT corresponde quando URL e chave sao literais adjacentes."""
    content = '"https://project.supabase.co","eyJabc.123.xyz"'
    config = parser.discover_config(content)
    assert config.url == "https://project.supabase.co"
    assert config.anon_key == "eyJabc.123.xyz"


@pytest.mark.unit
@pytest.mark.domain
def test_discover_config_not_found(parser):
    """Testa falha quando a anonKey esta ausente."""
    content = "nothing here"
    with pytest.raises(SupabaseConfigNotFoundError):
        parser.discover_config(content)


@pytest.mark.unit
@pytest.mark.domain
def test_extract_rest_tables(parser):
    """Testa extracao de tabelas REST."""
    content = '.from("profiles").from("posts")'
    endpoints = parser.extract_rest_tables(content)
    assert len(endpoints) == 8


@pytest.mark.unit
@pytest.mark.domain
def test_extract_auth_endpoints(parser):
    """Testa extracao de endpoints de Auth a partir de chamadas Mr."""
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
def test_extract_auth_endpoints_without_body(parser):
    """Endpoints de Auth sem objeto body ainda sao interpretados."""
    content = """
    Mr(this.fetch, "GET", `${this.url}/auth/v1/user`, {headers: {}});
    """
    endpoints = parser.extract_auth_endpoints(content)
    assert len(endpoints) == 1
    assert endpoints[0].body_keys == []


@pytest.mark.unit
@pytest.mark.domain
def test_extract_auth_admin_tag(parser):
    """Caminhos de auth admin recebem a tag auth-admin."""
    content = """
    Mr(this.fetch, "GET", `${this.url}/admin/users`, {headers: {}});
    """
    endpoints = parser.extract_auth_endpoints(content)
    assert len(endpoints) == 1
    assert endpoints[0].tag == "auth-admin"


@pytest.mark.unit
@pytest.mark.domain
def test_extract_auth_endpoints_duplicate(parser):
    """Testa deduplicacao de endpoints de Auth."""
    content = """
    Mr(this.fetch, "POST", `${this.url}/auth/v1/signup`, {body: {email: e}});
    Mr(this.fetch, "POST", `${this.url}/auth/v1/signup`, {body: {email: e}});
    """
    endpoints = parser.extract_auth_endpoints(content)
    assert len(endpoints) == 1


@pytest.mark.unit
@pytest.mark.domain
def test_extract_rpc_calls(parser):
    """Testa extracao de chamadas RPC."""
    content = '.rpc("get_user_profile")'
    endpoints = parser.extract_rpc_calls(content)
    assert len(endpoints) == 1
    assert endpoints[0].method == "POST"
    assert "rpc/get_user_profile" in endpoints[0].path


@pytest.mark.unit
@pytest.mark.domain
def test_extract_edge_functions(parser):
    """Testa extracao de Edge Functions."""
    content = "https://abc.supabase.co/functions/v1/heavy-task"
    endpoints = parser.extract_edge_functions(content)
    assert len(endpoints) == 1
    assert "functions/v1/heavy-task" in endpoints[0].path


@pytest.mark.unit
@pytest.mark.domain
def test_path_helpers(parser):
    """Testa helpers privados de interpretacao de caminhos."""
    assert parser._js_path_to_openapi("${this.id}") == "{id}"
    assert parser._extract_path_params("/{id}/info/{name}") == ["id", "name"]

    qparams = parser._extract_static_query("/path?a=1&b=2")
    assert len(qparams) == 2
    assert qparams[0].key == "a"
    assert qparams[0].value == "1"

    qparams_flag = parser._extract_static_query("/path?a=1&flag")
    assert len(qparams_flag) == 1
    assert qparams_flag[0].key == "a"
