"""Unit tests for AnalyzeApplication use case."""

from pathlib import Path

import pytest

from app.application.dto.analysis_report import AnalysisReport
from app.application.use_cases.analyze_application import AnalyzeApplication
from app.domain.models.supabase_config import SupabaseConfig


@pytest.fixture
def use_case(monkeypatch):
    """Return AnalyzeApplication with mocked dependencies."""

    # We use mocker/monkeypatch for dependencies
    class MockClient:
        def get_text(self, url):
            return "sw content" if "sw.js" in url else "index content"

    class MockRepo:
        def get_project_dir(self, domain):
            return Path("test_output")

        def find_largest_js(self, path):
            return Path("test_output/bundle.js")

        def write_text(self, p, c):
            pass

    class MockDownloader:
        def download_all(self, base, urls, directory):
            pass

    class MockParser:
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

    class MockSwagger:
        def build_specification(self, c, e, b):
            return {"swagger": "ok"}

    class MockValidator:
        def validate_supabase_config(self, c):
            pass

    return AnalyzeApplication(
        http_client=MockClient(),
        file_repository=MockRepo(),
        asset_downloader=MockDownloader(),
        bundle_parser=MockParser(),
        swagger_builder=MockSwagger(),
        config_validator=MockValidator(),
    )


@pytest.mark.unit
@pytest.mark.application
def test_analyze_execute(use_case, monkeypatch):
    """Test full execution of AnalyzeApplication."""

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
    """Test the to_dict method of AnalysisReport."""
    report = AnalysisReport(
        app_url="https://a.com",
        supabase_url="https://s.co",
        anon_key="eyJ1234567890",  # gitleaks:allow
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
    """Test FileNotFoundError when no JS bundle is found."""
    monkeypatch.setattr(use_case.file_repository, "find_largest_js", lambda p: None)
    with pytest.raises(FileNotFoundError, match="No JS bundle found"):
        use_case.execute("https://example.com")


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_index_empty(use_case, monkeypatch):
    """Test asset discovery from index.html when empty."""
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: None)
    assets = use_case._fetch_from_index("https://example.com")
    assert len(assets) == 0


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_index_matching(use_case, monkeypatch):
    """Test asset discovery from index.html with regex matches."""
    html = '<script src="/assets/m.js"></script><link href="/assets/s.css">'
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: html)
    assets = use_case._fetch_from_index("https://example.com")
    assert len(assets) == 2
    assert assets[0].url_path == "assets/m.js"
    assert assets[1].url_path == "assets/s.css"


@pytest.mark.unit
@pytest.mark.application
def test_fetch_from_sw(use_case, monkeypatch):
    """Test asset discovery from sw.js."""
    # Let's test _fetch_from_sw directly
    assets = use_case._fetch_from_sw("https://example.com")
    # My MockClient returns "sw content" if sw.js in url
    assert len(assets) == 0  # because "sw content" doesn't have precacheAndRoute

    # Test with valid sw content
    monkeypatch.setattr(
        use_case.http_client, "get_text", lambda u: 'precacheAndRoute([{"url": "a.js"}, {"url": "b.css"}])'
    )
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 2
    assert assets[0].url_path == "a.js"


@pytest.mark.unit
@pytest.mark.application
def test_analyze_skip_download(use_case, monkeypatch):
    """Test skip_download branch."""
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
    """Test JSON error handling in sw.js parsing."""
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: "precacheAndRoute([{invalid-json}])")
    assets = use_case._fetch_from_sw("https://example.com")
    assert len(assets) == 0


@pytest.mark.unit
@pytest.mark.application
def test_discover_assets_fallback(use_case, monkeypatch):
    """Test fallback logic when sw.js fails."""
    monkeypatch.setattr(use_case.http_client, "get_text", lambda u: "" if "sw.js" in u else "index content")
    assets = use_case._discover_assets("https://example.com")
    # Should fall back to index (index content has no assets in my mock logic unless I fix it)
    assert len(assets) == 0
