"""Fixtures e configuracao global do pytest."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import pytest

from recon.infrastructure.logging_config import configure_logging


@pytest.fixture(autouse=True)
def _configure_structlog() -> None:
    """Evita erros ao instanciar UrllibHttpClient e orquestrador nos testes."""
    configure_logging(json_logs=True)


@pytest.fixture
def fake_jwt() -> str:
    """JWT fictício com três segmentos (formato anon Supabase)."""
    return "eyJhbGciOiJIUzI1NiJ9.eyJhIjoxfQ.zzz"


@pytest.fixture
def minimal_bundle_js(fake_jwt: str) -> str:
    """Fragmento JS com URL Supabase, anon, tabela, RPC e edge function."""
    return "\n".join(
        [
            'const api = "https://projunit.supabase.co"',
            f'const key = "{fake_jwt}"',
            '.from("users")',
            '.rpc("count_rows")',
            "supabase.co/functions/v1/hello_edge",
        ]
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Marca testes sob tests/unit como @pytest.mark.unit."""
    _ = config
    for item in items:
        raw = getattr(item, "path", None) or getattr(item, "fspath", None)
        parts = Path(str(raw)).resolve().parts
        try:
            i = parts.index("tests")
            suite = parts[i + 1] if i + 1 < len(parts) else ""
        except ValueError:
            suite = ""
        if suite == "unit":
            item.add_marker(pytest.mark.unit)
