"""Ponto de entrada: carrega configuracao e executa o analisador."""

import json
import logging
import os
import sys
from pathlib import Path

import yaml

from recon_paths import REPO_ROOT, repo_path
from src.application.use_cases.analyze_application import AnalyzeApplication
from src.application.use_cases.test_api_reliability import ApiReliabilityTester
from src.domain.exceptions import DomainError
from src.domain.services.bundle_parser import BundleParserService
from src.domain.services.swagger_builder import SwaggerBuilderService
from src.domain.validation.config_validator import ConfigValidator
from src.infrastructure.loaders.asset_downloader import AssetDownloader
from src.infrastructure.network.http_client import HTTPClient
from src.infrastructure.persistence.file_repository import FileRepository
from src.presentation.cli.arguments import parse_args
from src.presentation.cli.terminal_ui import TerminalUI


logger = logging.getLogger(__name__)


def bootstrap() -> None:
    """Initialize and run the application."""
    ui = TerminalUI()
    args = parse_args()

    config_path = repo_path("config", "settings.json")
    with config_path.open(encoding="utf-8") as f:
        config = json.load(f)

    output_dir = config.get("output", {}).get("base_path", "output")
    http_timeout = config.get("http", {}).get("timeout_seconds", 30)

    http_client = HTTPClient(timeout=http_timeout)
    file_repo = FileRepository(base_output_path=str(repo_path(output_dir)))
    downloader = AssetDownloader(http_client, file_repo)
    parser = BundleParserService()
    builder = SwaggerBuilderService()
    validator = ConfigValidator()

    analyzer = AnalyzeApplication(
        http_client=http_client,
        file_repository=file_repo,
        asset_downloader=downloader,
        bundle_parser=parser,
        swagger_builder=builder,
        config_validator=validator,
    )
    tester = ApiReliabilityTester(http_client=http_client)

    try:
        ui.print_info(f"Initiating analysis for: [bold]{args.url}[/bold]")
        report = analyzer.execute(app_url=args.url, skip_download=args.skip_download)
        ui.display_report(report)

        if not args.no_test:
            ui.print_info("Initiating endpoint reliability tests...")
            test_methods = {m.strip().upper() for m in args.methods.split(",")}
            swagger_spec = yaml.safe_load(Path(report.swagger_path).read_text(encoding="utf-8"))
            results = tester.execute(
                swagger_spec=swagger_spec,
                anon_key=report.anon_key,
                methods_to_test=test_methods,
            )
            ui.display_test_results(results)

        ui.print_info("[bold green]Process completed successfully.[/bold green]")

    except DomainError as e:
        ui.print_error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception("An unexpected error occurred")
        ui.print_error(f"Unexpected error: {e}")
        sys.exit(1)


def main() -> None:
    """Carrega configuracao e inicia o pipeline de analise."""
    os.chdir(REPO_ROOT)
    logging.basicConfig(level=logging.INFO)
    bootstrap()


if __name__ == "__main__":
    main()
