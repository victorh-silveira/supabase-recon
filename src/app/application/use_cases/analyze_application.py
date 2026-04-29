"""Use case for analyzing a Lovable/Supabase application."""

import json
import logging
import re

import yaml

from app.application.dto.analysis_report import AnalysisReport
from app.domain.models.asset import Asset
from app.domain.services.bundle_parser import BundleParserService
from app.domain.services.swagger_builder import SwaggerBuilderService
from app.domain.validation.config_validator import ConfigValidator
from app.infrastructure.loaders.asset_downloader import AssetDownloader
from app.infrastructure.network.http_client import HTTPClient
from app.infrastructure.persistence.file_repository import FileRepository


logger = logging.getLogger(__name__)


class AnalyzeApplication:
    """Orchestrates the process of downloading and analyzing a Supabase application."""

    def __init__(
        self,
        http_client: HTTPClient,
        file_repository: FileRepository,
        asset_downloader: AssetDownloader,
        bundle_parser: BundleParserService,
        swagger_builder: SwaggerBuilderService,
        config_validator: ConfigValidator,
    ):
        """Initialize with required services."""
        self.http_client = http_client
        self.file_repository = file_repository
        self.asset_downloader = asset_downloader
        self.bundle_parser = bundle_parser
        self.swagger_builder = swagger_builder
        self.config_validator = config_validator

    def execute(self, app_url: str, *, skip_download: bool = False) -> AnalysisReport:
        """Run the full analysis pipeline."""
        base_url = app_url.rstrip("/")
        domain = re.sub(r"http[s]?://", "", base_url).split("/")[0]
        project_dir = self.file_repository.get_project_dir(domain)

        # 1. Discovery
        if skip_download and project_dir.exists():
            logger.info(f"Skipping download, using existing assets in {project_dir}")
        else:
            assets = self._discover_assets(base_url)
            self.asset_downloader.download_all(base_url, assets, project_dir)

        # 2. Heuristics: Find main JS bundle
        main_bundle = self.file_repository.find_largest_js(project_dir)
        if not main_bundle:
            raise FileNotFoundError(f"No JS bundle found in {project_dir}")

        bundle_content = main_bundle.read_text(encoding="utf-8", errors="replace")
        bundle_stats = main_bundle.stat()

        # 3. Extraction
        config = self.bundle_parser.discover_config(bundle_content)
        self.config_validator.validate_supabase_config(config)

        auth_eps = self.bundle_parser.extract_auth_endpoints(bundle_content)
        tables = self.bundle_parser.extract_rest_tables(bundle_content)
        rpcs = self.bundle_parser.extract_rpc_calls(bundle_content)
        edge_fns = self.bundle_parser.extract_edge_functions(bundle_content)

        # 4. Specification
        all_endpoints = auth_eps + tables + rpcs + edge_fns
        swagger = self.swagger_builder.build_specification(config, all_endpoints, app_url)

        # 5. Output
        swagger_path = project_dir / "swagger.yaml"
        yaml_content = yaml.dump(swagger, allow_unicode=True, sort_keys=False)
        self.file_repository.write_text(swagger_path, yaml_content)

        return AnalysisReport(
            app_url=app_url,
            supabase_url=config.url,
            anon_key=config.anon_key,
            auth_endpoints_count=len(auth_eps),
            rest_tables_count=len({ep.path for ep in tables}),
            rpc_calls_count=len(rpcs),
            edge_functions_count=len(edge_fns),
            swagger_path=str(swagger_path.resolve()),
            bundle_name=main_bundle.name,
            bundle_size_kb=bundle_stats.st_size / 1024,
            detected_assets_count=len(list(project_dir.rglob("*"))),
        )

    def _discover_assets(self, base_url: str) -> list[Asset]:
        """Discovery logic: try sw.js, then fallback to index.html."""
        assets = self._fetch_from_sw(base_url)
        if not assets:
            logger.info("Falling back to index.html for asset extraction...")
            assets = self._fetch_from_index(base_url)
        return assets

    def _fetch_from_sw(self, base_url: str) -> list[Asset]:
        """Extract assets from precacheAndRoute in sw.js."""
        sw_url = f"{base_url}/sw.js"
        content = self.http_client.get_text(sw_url)
        if not content:
            return []

        match = re.search(r"precacheAndRoute\((\[.*?\])", content, re.DOTALL)
        if not match:
            return []

        raw_json = match.group(1)
        # Fix JS object literal to valid JSON
        raw_json = re.sub(r"([{,])\s*(\w+)\s*:", r'\1"\2":', raw_json)
        raw_json = re.sub(r",\s*([}\]])", r"\1", raw_json)

        try:
            entries = json.loads(raw_json)
            return [Asset(url_path=e["url"]) for e in entries if "url" in e]
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse sw.js assets: {e}")
            return []

    def _fetch_from_index(self, base_url: str) -> list[Asset]:
        """Extract assets from index.html using regex."""
        content = self.http_client.get_text(f"{base_url}/")
        if not content:
            return []

        seen: set[str] = set()
        assets = []
        # Pattern for typical assets in Lovable apps
        for match in re.finditer(r'(?:src|href)=["\'`](/assets/[^"\'`]+)["\'`]', content):
            u = match.group(1)
            if u not in seen:
                seen.add(u)
                assets.append(Asset(url_path=u.lstrip("/")))
        return assets
