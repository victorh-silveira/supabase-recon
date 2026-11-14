"""Testes unitarios para o caso de uso AnalyzeApplication."""

from pathlib import Path

import pytest

from application.dto.analysis_report import AnalysisReport
from application.use_cases.analyze_application import AnalyzeApplication
from domain.entities.supabase_config import SupabaseConfig


@pytest.fixture
def use_case():
    """Retorna AnalyzeApplication com implementacoes falsas das portas."""

    class FakeClient:
        def get_text(self, url):
            return "sw content" if "sw.js" in url else "index content"

        def get_bytes(self, url):
            return b"content"

        def request(self, method, url, headers=None, json_data=None):
            return 200, "OK", "{}"

    class FakeRepo:
        def get_project_dir(self, domain):
            return Path("test_output")

        def find_largest_js(self, path):
            return Path("test_output/bundle.js")

        def write_text(self, p, c):
            return None

        def write_bytes(self, p, c):
            return None

    class FakeDownloader:
        def download_all(self, base, urls, directory):
            return []

    class FakeParser:
        def discover_config(self, c):
            return SupabaseConfig("https://s.co", "key")

        def extract_auth_endpoints(self, c):
            return []

        def extract_rest_tables(self, c):
            return []

        def extract_rpc_calls(self, c):
            return []

        def extract_edge_functions(self, c):
            return []

    class FakeSwagger:
        def build_specification(self, c, e, b):
            return {"swagger": "ok"}

    class FakeValidator:
        def validate_supabase_config(self, c):
            return None

    return AnalyzeApplication(
        http_client=FakeClient(),
        file_repository=FakeRepo(),
        asset_downloader=FakeDownloader(),
        bundle_parser=FakeParser(),
        swagger_builder=FakeSwagger(),
        config_validator=FakeValidator(),
    )


@pytest.mark.unit
@pytest.mark.application
def test_analyze_execute(use_case, monkeypatch):
    """Testa execucao completa de AnalyzeApplication."""

    class MockStat:
        st_size = 1024

    monkeypatch.setattr("pathlib.Path.read_text", lambda *args, **kwargs: "js content")
    monkeypatch.setattr("pathlib.Path.write_text", lambda *args, **kwargs: 10)
    monkeypatch.setattr("pathlib.Path.resolve", lambda self: self)
    monkeypatch.setattr("pathlib.Path.stat", lambda self: MockStat())
    monkeypatch.setattr("pathlib.Path.exists", lambda self: True)
    monkeypatch.setattr("pathlib.Path.rglob", lambda self, p: [Path("file1")])

    report = use_case.execute(app_url="https://example.com")
    assert report.app_url == "https://example.com"
    assert report.bundle_size_kb == 1.0


@pytest.mark.unit
@pytest.mark.application
def test_analysis_report_to_dict():
    """Testa o metodo to_dict de AnalysisReport."""
    report = AnalysisReport(
        app_url="https://a.com",
        supabase_url="https://s.co",
        anon_key="eyJ1234567890",
        auth_endpoints_count=1,
        rest_tables_count=2,
        rpc_calls_count=3,
        edge_functions_count=4,
        swagger_path="path/to/swagger.yaml",
        bundle_name="bundle.js",
        bundle_size_kb=10.0,
        detected_assets_count=5,
    )
    d = report.to_dict()
    assert d["app_url"] == "https://a.com"
    assert "eyJ1234567..." in d["anon_key"]
    assert d["stats"]["rpc_calls"] == 3


@pytest.mark.unit
@pytest.mark.application
def test_analyze_no_bundle_error(use_case, monkeypatch):
    """Testa FileNotFoundError quando nenhum bundle JS e encontrado."""
    monkeypatch.setattr(use_case.file_repository, "find_largest_js", lambda p: None)
    with pytest.raises(FileNotFoundError, match="No JS bundle found"):
        use_case.execute("https://example.com")


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_index_empty(use_case, monkeypatch):
    """Testa descoberta de assets em index.html quando vazio."""
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: None)
    assets = use_case._fetch_from_index("https://example.com")
    assert len(assets) == 0


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_index_matching(use_case, monkeypatch):
    """Testa descoberta de assets em index.html com correspondencias regex."""
    html = '<script src="/assets/m.js"></script><link href="/assets/s.css">'
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: html)
    assets = use_case._fetch_from_index("https://example.com")
    assert len(assets) == 2
    assert assets[0].url_path == "assets/m.js"
    assert assets[1].url_path == "assets/s.css"


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_sw(use_case, monkeypatch):
    """Testa descoberta de assets a partir de sw.js."""
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 0

    monkeypatch.setattr(
        use_case.http_client, "get_text", lambda u: 'precacheAndRoute([{"url": "a.js"}, {"url": "b.css"}])'
    )
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 2
    assert assets[0].url_path == "a.js"


@pytest.mark.unit
@pytest.mark.application
def test_analyze_skip_download(use_case, monkeypatch):
    """Testa o ramo skip_download."""
    monkeypatch.setattr("pathlib.Path.exists", lambda self: True)
    monkeypatch.setattr("pathlib.Path.read_text", lambda *args, **kwargs: "js content")
    monkeypatch.setattr("pathlib.Path.stat", lambda self: type("S", (), {"st_size": 10})())
    monkeypatch.setattr("pathlib.Path.rglob", lambda self, p: [])
    monkeypatch.setattr("pathlib.Path.resolve", lambda self: self)

    report = use_case.execute(app_url="https://example.com", skip_download=True)
    assert report.app_url == "https://example.com"


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_sw_json_error(use_case, monkeypatch):
    """Testa tratamento de erro JSON ao interpretar sw.js."""
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: "precacheAndRoute([{invalid-json}])")
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 0


@pytest.mark.unit
@pytest.mark.application
def test_discover_assets_fallback(use_case, monkeypatch):
    """Testa logica de fallback quando sw.js falha."""
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: "" if "sw.js" in u else "index content")
    assets = use_case._discover_assets("https://example.com")
    assert len(assets) == 0


@pytest.mark.unit
@pytest.mark.application
def test_discover_assets_from_sw(use_case, monkeypatch):
    """Descoberta nao vazia em sw.js ignora o fallback de index.html."""
    monkeypatch.setattr(
        use_case.http_client,
        "get_text",
        lambda u: 'precacheAndRoute([{"url": "main.js"}])',
    )
    assets = use_case._discover_assets("https://example.com")
    assert len(assets) == 1
    assert assets[0].url_path == "main.js"


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_index_deduplicates(use_case, monkeypatch):
    """URLs de assets duplicadas em index.html sao ignoradas."""
    html = '<script src="/assets/m.js"></script><script src="/assets/m.js"></script>'
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: html)
    assets = use_case._fetch_from_index("https://example.com")
    assert len(assets) == 1


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_sw_type_error(use_case, monkeypatch):
    """Entradas de precache que nao sao dicionarios sao ignoradas."""
    monkeypatch.setattr(
        use_case.http_client,
        "get_text",
        lambda u: "precacheAndRoute([1])",
    )
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 0


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_sw_non_list_json(use_case, monkeypatch):
    """Payload JSON que nao e lista nao retorna assets."""
    monkeypatch.setattr(
        use_case.http_client,
        "get_text",
        lambda u: 'precacheAndRoute([{"url": "a.js"}])',
    )
    monkeypatch.setattr(
        "application.use_cases.analyze_application.json.loads",
        lambda raw: {"url": "a.js"},
    )
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 0
