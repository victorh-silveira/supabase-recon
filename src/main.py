"""Main entrypoint for Chupabase Analyzer."""

import logging
import sys
from pathlib import Path

import yaml

from app.application.use_cases.analyze_application import AnalyzeApplication
from app.application.use_cases.test_api_reliability import ApiReliabilityTester
from app.domain.exceptions import DomainError
from app.domain.services.bundle_parser import BundleParserService
from app.domain.services.swagger_builder import SwaggerBuilderService
from app.domain.validation.config_validator import ConfigValidator
from app.infrastructure.loaders.asset_downloader import AssetDownloader
from app.infrastructure.network.http_client import HTTPClient
from app.infrastructure.persistence.file_repository import FileRepository
from app.interfaces.cli.arguments import parse_args
from app.interfaces.cli.terminal_ui import TerminalUI


logger = logging.getLogger(__name__)


def bootstrap():
    """Initialize and run the application."""
    ui = TerminalUI()
    args = parse_args()

    # 1. Dependency Injection (Manual)
    http_client = HTTPClient()
    file_repo = FileRepository()
    downloader = AssetDownloader(http_client, file_repo)
    parser = BundleParserService()
    builder = SwaggerBuilderService()
    validator = ConfigValidator()

    # Use Cases
    analyzer = AnalyzeApplication(
        http_client=http_client,
        file_repository=file_repo,
        asset_downloader=downloader,
        bundle_parser=parser,
        swagger_builder=builder,
        config_validator=validator,
    )
    tester = ApiReliabilityTester(http_client=http_client)

    # 2. Execution
    try:
        # Step A: Analysis
        ui.print_info(f"Initiating analysis for: [bold]{args.url}[/bold]")
        report = analyzer.execute(app_url=args.url, skip_download=args.skip_download)
        ui.display_report(report)

        # Step B: Testing (Optional)
        if not args.no_test:
            ui.print_info("Initiating endpoint reliability tests...")
            test_methods = {m.strip().upper() for m in args.methods.split(",")}

            # Load the generated spec back (or use the dict from analyzer)
            # For simplicity, we assume analyzer.execute could return the dict,
            # but here we'll just use the report data if we had it, or re-run builder.
            # Actually, AnalyzeApplication could return both report and spec for efficiency.
            # For now, let's keep it clean.

            # To avoid re-running analysis, we'll assume AnalyzeApplication
            # logic is available or we re-read the YAML.
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


if __name__ == "__main__":
    bootstrap()
