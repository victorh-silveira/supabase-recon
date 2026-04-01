"""Testes do orquestrador (com portas falsas)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from recon.application.recon_orchestrator import (
    ReconOptions,
    ReconOrchestrator,
    download_assets,
    fetch_index_asset_urls,
    fetch_precache_urls,
    find_main_js_bundle,
    resolve_recon_paths,
)
from recon.domain.exceptions import BundleNotFoundError, MissingAnonKeyError


def test_resolve_recon_paths_uses_host_and_output_root(tmp_path: Path) -> None:
    """Deriva pasta output estável a partir da URL."""
    root = tmp_path / "custom_output"
    paths = resolve_recon_paths("https://my.app:8443/foo", output_root=root)
    assert paths.output_dir == root / "my.app_8443"
    assert paths.swagger_file.name == "swagger.yaml"


def test_find_main_js_bundle_picks_largest_in_assets(tmp_path: Path) -> None:
    """Entre vários JS em assets, escolhe o maior."""
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "small.js").write_bytes(b"x" * 10)
    (assets / "big.js").write_bytes(b"y" * 50)
    assert find_main_js_bundle(tmp_path) == assets / "big.js"


def test_find_main_js_bundle_fallback_rglob(tmp_path: Path) -> None:
    """Sem pasta assets, procura recursivamente."""
    deep = tmp_path / "nested"
    deep.mkdir(parents=True)
    (deep / "only.js").write_text("void 0", encoding="utf-8")
    assert find_main_js_bundle(tmp_path) == deep / "only.js"


def test_find_main_js_bundle_raises_when_empty(tmp_path: Path) -> None:
    """Sem ficheiros .js levanta BundleNotFoundError."""
    with pytest.raises(BundleNotFoundError):
        find_main_js_bundle(tmp_path)


def test_fetch_precache_urls_parses_sw_js() -> None:
    """Service worker com precacheAndRoute válido devolve URLs."""
    base = "https://demo.local"
    sw_body = 'precacheAndRoute([{url:"assets/main.js"},{url:"assets/other.js"}])'
    http = MagicMock()
    http.get_text.side_effect = lambda url: sw_body if url.endswith("/sw.js") else None
    log = MagicMock()
    urls = fetch_precache_urls(base, http, log)
    assert urls == ["assets/main.js", "assets/other.js"]


def test_fetch_index_asset_urls_from_html() -> None:
    """Fallback index.html extrai href/src /assets/...."""
    html = '<!DOCTYPE html><script src="/assets/chunk.js"></script>'
    http = MagicMock()
    http.get_text.return_value = html
    log = MagicMock()
    urls = fetch_index_asset_urls("https://x", http, log)
    assert urls == ["assets/chunk.js"]


def test_download_assets_writes_files(tmp_path: Path) -> None:
    """Cada URL descarregada escreve ficheiro relativo ao out_dir."""
    http = MagicMock()
    http.get_bytes.return_value = b"data"
    log = MagicMock()
    download_assets("https://h", ["assets/a.js"], tmp_path, http, log)
    assert (tmp_path / "assets" / "a.js").read_bytes() == b"data"


def test_orchestrator_happy_path_skip_download(tmp_path: Path, minimal_bundle_js: str) -> None:
    """Pipeline completo com skip-download e directoria pré-preenchida."""
    out = tmp_path / "out" / "app_host"
    assets = out / "assets"
    assets.mkdir(parents=True)
    (assets / "bundle.js").write_text(minimal_bundle_js, encoding="utf-8")

    writer = MagicMock()
    probe = MagicMock()
    http_text = MagicMock()
    http_bytes = MagicMock()

    orch = ReconOrchestrator(
        http_text=http_text,
        http_bytes=http_bytes,
        spec_writer=writer,
        endpoint_probe=probe,
        log=MagicMock(),
    )
    opts = ReconOptions(
        app_url="https://app_host",
        skip_download_if_existing=True,
        run_endpoint_probe=False,
        probe_methods=frozenset({"get"}),
    )
    analysis = orch.run(opts, output_root=tmp_path / "out")

    assert analysis.supabase.base_url == "https://projunit.supabase.co"
    writer.write_yaml.assert_called_once()
    probe.run_probes.assert_not_called()
    args, _kwargs = writer.write_yaml.call_args
    assert args[0].name == "swagger.yaml"
    assert "openapi" in args[1]


def test_orchestrator_propagates_missing_anon(tmp_path: Path) -> None:
    """Bundle sem JWT levanta MissingAnonKeyError."""
    out = tmp_path / "o" / "host_x"
    (out / "assets").mkdir(parents=True)
    (out / "assets" / "x.js").write_text("console.log(1)", encoding="utf-8")

    orch = ReconOrchestrator(
        http_text=MagicMock(),
        http_bytes=MagicMock(),
        spec_writer=MagicMock(),
        endpoint_probe=MagicMock(),
        log=MagicMock(),
    )
    opts = ReconOptions(
        app_url="https://host_x",
        skip_download_if_existing=True,
        run_endpoint_probe=False,
        probe_methods=frozenset(),
    )
    with pytest.raises(MissingAnonKeyError):
        orch.run(opts, output_root=tmp_path / "o")


def test_orchestrator_calls_probe_when_enabled(tmp_path: Path, minimal_bundle_js: str) -> None:
    """Com run_endpoint_probe=True chama a porta de sondagem."""
    out = tmp_path / "z" / "h"
    (out / "assets").mkdir(parents=True)
    (out / "assets" / "b.js").write_text(minimal_bundle_js, encoding="utf-8")

    probe = MagicMock()
    orch = ReconOrchestrator(
        http_text=MagicMock(),
        http_bytes=MagicMock(),
        spec_writer=MagicMock(),
        endpoint_probe=probe,
        log=MagicMock(),
    )
    opts = ReconOptions(
        app_url="https://h",
        skip_download_if_existing=True,
        run_endpoint_probe=True,
        probe_methods=frozenset({"get"}),
    )
    orch.run(opts, output_root=tmp_path / "z")
    probe.run_probes.assert_called_once()
