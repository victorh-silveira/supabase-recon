"""Composition root: Settings, adapters, use cases and CLI execution."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import yaml

from application.use_cases.analyze_application import AnalyzeApplication
from application.use_cases.test_api_reliability import ApiReliabilityTester
from domain.exceptions import DomainError
from domain.services.bundle_parser import BundleParserService
from domain.services.swagger_builder import SwaggerBuilderService
from domain.validation.config_validator import ConfigValidator
from infrastructure.adapters.asset_downloader import AssetDownloader
from infrastructure.adapters.file_repository import FileRepository
from infrastructure.adapters.http_client import HTTPClient
from infrastructure.config.settings import Settings
from infrastructure.logging.events import log_event
from presentation.cli.arguments import parse_args
from presentation.cli.terminal_ui import TerminalUI
from presentation.logging.setup import configure_logging


logger = logging.getLogger(__name__)


def bootstrap(repo_root: Path) -> None:
    """Wire dependencies and run the analysis pipeline."""
    settings = Settings.from_env(repo_root)
    configure_logging(settings.log_level)

    ui = TerminalUI()
    args = parse_args()

    output_dir = repo_root / settings.output_base_path
    http_client = HTTPClient(timeout=settings.http_timeout_seconds)
    file_repo = FileRepository(base_output_path=str(output_dir))
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

    log_event(logger, logging.INFO, "recon.run.started", url=args.url)
    try:
        ui.print_info(f"Initiating analysis for: [bold]{args.url}[/bold]")
        if args.skip_download:
            log_event(logger, logging.INFO, "recon.analyze.skipped_download", url=args.url)

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

        log_event(logger, logging.INFO, "recon.run.finished", url=args.url)
        ui.print_info("[bold green]Process completed successfully.[/bold green]")

    except DomainError as e:
        log_event(logger, logging.ERROR, "recon.run.failed", url=args.url, error=str(e))
        ui.print_error(str(e))
        sys.exit(1)
    except Exception as e:
        log_event(
            logger,
            logging.ERROR,
            "recon.run.failed",
            url=args.url,
            error=str(e),
            exc_info=True,
        )
        ui.print_error(f"Unexpected error: {e}")
        sys.exit(1)


def main(repo_root: Path) -> None:
    """Entrypoint used by app/run.py."""
    bootstrap(repo_root)
