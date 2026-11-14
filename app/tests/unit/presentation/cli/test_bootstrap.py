"""Testes unitarios para o composition root da CLI."""

import pytest

from application.dto.analysis_report import AnalysisReport
from domain.exceptions import ValidationError
from presentation.cli import bootstrap


@pytest.mark.unit
@pytest.mark.presentation
def test_bootstrap_success(monkeypatch, tmp_path):
    """Caminho feliz conecta dependencias e finaliza."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setattr(
        "sys.argv",
        ["bootstrap", "--url", "https://example.com", "--no-test"],
    )

    report = AnalysisReport(
        app_url="https://example.com",
        supabase_url="https://s.co",
        anon_key="eyJkey",
        auth_endpoints_count=0,
        rest_tables_count=0,
        rpc_calls_count=0,
        edge_functions_count=0,
        swagger_path=str(tmp_path / "swagger.yaml"),
        bundle_name="b.js",
        bundle_size_kb=1.0,
        detected_assets_count=1,
    )

    class FakeAnalyzer:
        def execute(self, app_url, *, skip_download=False):
            return report

    class FakeUI:
        def print_info(self, message):
            return None

        def print_error(self, message):
            return None

        def display_report(self, report):
            return None

        def display_test_results(self, results):
            return None

    monkeypatch.setattr(bootstrap, "TerminalUI", FakeUI)
    monkeypatch.setattr(bootstrap, "AnalyzeApplication", lambda **kwargs: FakeAnalyzer())
    monkeypatch.setattr(bootstrap, "ApiReliabilityTester", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "HTTPClient", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "FileRepository", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "AssetDownloader", lambda *a, **k: object())
    monkeypatch.setattr(bootstrap, "BundleParserService", lambda: object())
    monkeypatch.setattr(bootstrap, "SwaggerBuilderService", lambda: object())
    monkeypatch.setattr(bootstrap, "ConfigValidator", lambda: object())

    bootstrap.bootstrap(tmp_path)


@pytest.mark.unit
@pytest.mark.presentation
def test_bootstrap_domain_error(monkeypatch, tmp_path):
    """DomainError encerra com codigo 1."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setattr("sys.argv", ["bootstrap", "--url", "https://example.com", "--no-test"])

    class FailingAnalyzer:
        def execute(self, app_url, *, skip_download=False):
            raise ValidationError("bad config")

    class FakeUI:
        def print_info(self, message):
            return None

        def print_error(self, message):
            return None

        def display_report(self, report):
            return None

        def display_test_results(self, results):
            return None

    monkeypatch.setattr(bootstrap, "TerminalUI", FakeUI)
    monkeypatch.setattr(bootstrap, "AnalyzeApplication", lambda **kwargs: FailingAnalyzer())
    monkeypatch.setattr(bootstrap, "ApiReliabilityTester", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "HTTPClient", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "FileRepository", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "AssetDownloader", lambda *a, **k: object())
    monkeypatch.setattr(bootstrap, "BundleParserService", lambda: object())
    monkeypatch.setattr(bootstrap, "SwaggerBuilderService", lambda: object())
    monkeypatch.setattr(bootstrap, "ConfigValidator", lambda: object())

    with pytest.raises(SystemExit) as exc:
        bootstrap.bootstrap(tmp_path)
    assert exc.value.code == 1


@pytest.mark.unit
@pytest.mark.presentation
def test_bootstrap_unexpected_error(monkeypatch, tmp_path):
    """Erros inesperados encerram com codigo 1."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setattr("sys.argv", ["bootstrap", "--url", "https://example.com", "--no-test"])

    class FailingAnalyzer:
        def execute(self, app_url, *, skip_download=False):
            raise RuntimeError("boom")

    class FakeUI:
        def print_info(self, message):
            return None

        def print_error(self, message):
            return None

        def display_report(self, report):
            return None

        def display_test_results(self, results):
            return None

    monkeypatch.setattr(bootstrap, "TerminalUI", FakeUI)
    monkeypatch.setattr(bootstrap, "AnalyzeApplication", lambda **kwargs: FailingAnalyzer())
    monkeypatch.setattr(bootstrap, "ApiReliabilityTester", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "HTTPClient", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "FileRepository", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "AssetDownloader", lambda *a, **k: object())
    monkeypatch.setattr(bootstrap, "BundleParserService", lambda: object())
    monkeypatch.setattr(bootstrap, "SwaggerBuilderService", lambda: object())
    monkeypatch.setattr(bootstrap, "ConfigValidator", lambda: object())

    with pytest.raises(SystemExit) as exc:
        bootstrap.bootstrap(tmp_path)
    assert exc.value.code == 1


@pytest.mark.unit
@pytest.mark.presentation
def test_bootstrap_with_tests(monkeypatch, tmp_path):
    """Ramo de testes de confiabilidade e exercitado."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setattr("sys.argv", ["bootstrap", "--url", "https://example.com", "--skip-download"])

    swagger = tmp_path / "swagger.yaml"
    swagger.write_text("openapi: 3.0.3\npaths: {}\nservers:\n  - url: https://s.co\n", encoding="utf-8")

    report = AnalysisReport(
        app_url="https://example.com",
        supabase_url="https://s.co",
        anon_key="eyJkey",
        auth_endpoints_count=0,
        rest_tables_count=0,
        rpc_calls_count=0,
        edge_functions_count=0,
        swagger_path=str(swagger),
        bundle_name="b.js",
        bundle_size_kb=1.0,
        detected_assets_count=1,
    )

    class FakeAnalyzer:
        def execute(self, app_url, *, skip_download=False):
            assert skip_download is True
            return report

    class FakeTester:
        def execute(self, swagger_spec, anon_key, methods_to_test):
            return []

    class FakeUI:
        def print_info(self, message):
            return None

        def print_error(self, message):
            return None

        def display_report(self, report):
            return None

        def display_test_results(self, results):
            return None

    monkeypatch.setattr(bootstrap, "TerminalUI", FakeUI)
    monkeypatch.setattr(bootstrap, "AnalyzeApplication", lambda **kwargs: FakeAnalyzer())
    monkeypatch.setattr(bootstrap, "ApiReliabilityTester", lambda **kwargs: FakeTester())
    monkeypatch.setattr(bootstrap, "HTTPClient", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "FileRepository", lambda **kwargs: object())
    monkeypatch.setattr(bootstrap, "AssetDownloader", lambda *a, **k: object())
    monkeypatch.setattr(bootstrap, "BundleParserService", lambda: object())
    monkeypatch.setattr(bootstrap, "SwaggerBuilderService", lambda: object())
    monkeypatch.setattr(bootstrap, "ConfigValidator", lambda: object())

    bootstrap.bootstrap(tmp_path)


@pytest.mark.unit
@pytest.mark.presentation
def test_main_calls_bootstrap(monkeypatch, tmp_path):
    """Main delega para bootstrap."""
    called = {}

    def fake_bootstrap(root):
        called["root"] = root

    monkeypatch.setattr(bootstrap, "bootstrap", fake_bootstrap)
    bootstrap.main(tmp_path)
    assert called["root"] == tmp_path
