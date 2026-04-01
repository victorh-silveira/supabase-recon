"""Caso de uso principal: descarregar assets, analisar bundle, gerar OpenAPI, sondar."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import structlog

from recon.application.ports import (
    EndpointProbePort,
    HttpBytesClientPort,
    HttpTextClientPort,
    JsonObjectWriterPort,
)
from recon.domain.bundle_analysis import analyze_bundle_content, normalize_app_base_url
from recon.domain.exceptions import BundleNotFoundError, MissingAnonKeyError
from recon.domain.models import BundleAnalysis, ReconPaths
from recon.domain.swagger_factory import build_openapi_spec


@dataclass(frozen=True, slots=True)
class ReconOptions:
    """Opções de linha de comando mapeadas para o orquestrador."""

    app_url: str
    skip_download_if_existing: bool
    run_endpoint_probe: bool
    probe_methods: frozenset[str]


def resolve_recon_paths(app_base_url: str, output_root: Path | None = None) -> ReconPaths:
    """Deriva `output/<host>/` e caminho do swagger."""
    root = output_root or Path("output")
    base = normalize_app_base_url(app_base_url)
    host = re.sub(r"http[s]?://", "", base).split("/")[0]
    domain = host.replace(":", "_")
    out_dir = root / domain
    return ReconPaths(output_dir=out_dir, swagger_file=out_dir / "swagger.yaml")


def find_main_js_bundle(out_dir: Path) -> Path:
    """Localiza o maior `.js` em `assets/` ou recursivamente."""
    assets = list((out_dir / "assets").glob("*.js"))
    if not assets:
        assets = list(out_dir.rglob("*.js"))
    if not assets:
        raise BundleNotFoundError(f"No .js file found under {out_dir}")
    return max(assets, key=lambda p: p.stat().st_size)


def fetch_precache_urls(base: str, http: HttpTextClientPort, log: structlog.BoundLogger) -> list[str]:
    """Extrai URLs do service worker `precacheAndRoute`."""
    sw_url = base + "/sw.js"
    log.info("recon.assets.precache_fetch", url=sw_url, phase="service_worker")
    content = http.get_text(sw_url)
    if not content:
        return []

    match = re.search(r"precacheAndRoute\((\[.*?\])", content, re.DOTALL)
    if not match:
        log.warning("recon.assets.precache_missing", url=sw_url, reason="precacheAndRoute_not_found")
        return []

    raw = match.group(1)
    raw = re.sub(r"([{,])\s*(\w+)\s*:", r'\1"\2":', raw)
    raw = re.sub(r",\s*([}\]])", r"\1", raw)

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as e:
        log.error("recon.assets.precache_json_invalid", error=str(e))
        return []

    seen: set[str] = set()
    urls: list[str] = []
    for entry in entries:
        u = entry.get("url", "")
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def fetch_index_asset_urls(base: str, http: HttpTextClientPort, log: structlog.BoundLogger) -> list[str]:
    """Fallback: extrai `/assets/...` do index HTML."""
    index_url = base + "/"
    log.info("recon.assets.index_fallback", url=index_url)
    content = http.get_text(index_url)
    if not content:
        log.error("recon.assets.index_failed", url=index_url)
        return []

    seen: set[str] = set()
    urls: list[str] = []
    for m in re.finditer(r'(?:src|href)=["\'`](/assets/[^"\'`]+)["\'`]', content):
        u = m.group(1)
        if u not in seen:
            seen.add(u)
            urls.append(u.lstrip("/"))
    return urls


def download_assets(
    base: str,
    urls: list[str],
    out_dir: Path,
    http: HttpBytesClientPort,
    log: structlog.BoundLogger,
) -> list[Path]:
    """Descarrega cada rota relativa para espelho em disco."""
    out_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for route in urls:
        full_url = base + "/" + route.lstrip("/")
        local = out_dir / Path(route.lstrip("/").replace("/", os.sep))
        local.parent.mkdir(parents=True, exist_ok=True)
        log.info("recon.assets.download_item", route=route, dest_url=full_url)
        data = http.get_bytes(full_url)
        if data is not None:
            local.write_bytes(data)
            downloaded.append(local)
    return downloaded


class ReconOrchestrator:
    """Orquestra portas de infra + regras de domínio."""

    def __init__(
        self,
        *,
        http_text: HttpTextClientPort,
        http_bytes: HttpBytesClientPort,
        spec_writer: JsonObjectWriterPort,
        endpoint_probe: EndpointProbePort,
        log: structlog.BoundLogger | None = None,
    ) -> None:
        """Compõe portas HTTP, persistência OpenAPI e sondagem opcional."""
        self._http_text = http_text
        self._http_bytes = http_bytes
        self._spec_writer = spec_writer
        self._endpoint_probe = endpoint_probe
        self._log = log or structlog.get_logger()

    def run(self, options: ReconOptions, output_root: Path | None = None) -> BundleAnalysis:
        """Executa o pipeline completo e devolve a análise do bundle."""
        base = normalize_app_base_url(options.app_url)
        paths = resolve_recon_paths(base, output_root)
        self._log.info(
            "recon.pipeline.start",
            app_base_url=base,
            output_dir=str(paths.output_dir),
            skip_download=options.skip_download_if_existing,
            probe_enabled=options.run_endpoint_probe,
        )

        if options.skip_download_if_existing and paths.output_dir.exists():
            self._log.info("recon.assets.skip_download", path=str(paths.output_dir))
        else:
            self._log.info("recon.assets.phase", step="download", app_base_url=base)
            urls = fetch_precache_urls(base, self._http_text, self._log)
            if not urls:
                self._log.info("recon.assets.fallback_index")
                urls = fetch_index_asset_urls(base, self._http_text, self._log)
            self._log.info("recon.assets.urls_resolved", count=len(urls))
            download_assets(base, urls, paths.output_dir, self._http_bytes, self._log)

        self._log.info("recon.bundle.locate", output_dir=str(paths.output_dir))
        try:
            js_file = find_main_js_bundle(paths.output_dir)
        except BundleNotFoundError:
            self._log.error("recon.bundle.not_found", output_dir=str(paths.output_dir))
            raise

        self._log.info(
            "recon.bundle.selected",
            path=str(js_file),
            size_kb=round(js_file.stat().st_size / 1024),
        )

        content = js_file.read_text(encoding="utf-8", errors="replace")
        try:
            analysis = analyze_bundle_content(content)
        except MissingAnonKeyError as e:
            self._log.error("recon.analysis.missing_anon_key", error=str(e))
            raise

        self._log.info(
            "recon.analysis.complete",
            supabase_url=analysis.supabase.base_url,
            anon_key_prefix=analysis.supabase.anon_key[:20],
            auth_endpoints=len(analysis.auth_endpoints),
            tables=len(analysis.tables),
            rpcs=len(analysis.rpcs),
            edge_functions=len(analysis.edge_functions),
        )

        openapi = build_openapi_spec(
            analysis.auth_endpoints,
            analysis.tables,
            analysis.rpcs,
            analysis.edge_functions,
            analysis.supabase.base_url,
            analysis.supabase.anon_key,
            base,
        )
        self._spec_writer.write_yaml(paths.swagger_file, openapi)
        self._log.info("recon.openapi.written", path=str(paths.swagger_file.resolve()))

        if options.run_endpoint_probe:
            self._endpoint_probe.run_probes(openapi, analysis.supabase.anon_key, options.probe_methods)

        return analysis
