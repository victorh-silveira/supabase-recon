"""Unit tests for TerminalUI."""

import pytest

from app.application.dto.analysis_report import AnalysisReport
from app.interfaces.cli import terminal_ui
from app.interfaces.cli.terminal_ui import TerminalUI


@pytest.fixture
def terminal_ui_instance():
    """Return an instance of TerminalUI."""
    return TerminalUI()


@pytest.mark.unit
@pytest.mark.interface
def test_print_info(terminal_ui_instance, monkeypatch):
    """Test print_info method."""
    printed_messages = []

    def mock_print(*args, **kwargs):
        printed_messages.append(args[0])

    monkeypatch.setattr(terminal_ui.console, "print", mock_print)

    terminal_ui_instance.print_info("Testing info message")
    assert any("INFO" in msg and "Testing info message" in msg for msg in printed_messages)


@pytest.mark.unit
@pytest.mark.interface
def test_print_error(terminal_ui_instance, monkeypatch):
    """Test print_error method."""
    printed_messages = []

    def mock_print(*args, **kwargs):
        printed_messages.append(args[0])

    monkeypatch.setattr(terminal_ui.console, "print", mock_print)

    terminal_ui_instance.print_error("Testing error message")
    assert any("ERROR" in msg and "Testing error message" in msg for msg in printed_messages)


@pytest.mark.unit
@pytest.mark.interface
def test_display_report(terminal_ui_instance, monkeypatch):
    """Test display_report method."""
    printed_messages = []

    def mock_print(*args, **kwargs):
        printed_messages.append(args[0])

    monkeypatch.setattr(terminal_ui.console, "print", mock_print)

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

    terminal_ui_instance.display_report(report)
    assert len(printed_messages) > 0


@pytest.mark.unit
@pytest.mark.interface
def test_display_test_results(terminal_ui_instance, monkeypatch):
    """Test display_test_results method."""
    printed_messages = []

    def mock_print(*args, **kwargs):
        printed_messages.append(args[0])

    monkeypatch.setattr(terminal_ui.console, "print", mock_print)

    # Empty results
    terminal_ui_instance.display_test_results([])
    assert len(printed_messages) == 0

    # Non-empty results
    results = [
        {"status": 200, "method": "GET", "path": "/rest/v1/users", "accessible": True, "reason": None},
        {"status": 403, "method": "POST", "path": "/rest/v1/posts", "accessible": False, "reason": "Forbidden"},
    ]
    terminal_ui_instance.display_test_results(results)
    assert len(printed_messages) > 0
