"""Premium Terminal UI using Rich."""

import logging
from typing import Any

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from app.application.dto.analysis_report import AnalysisReport


# Configure logging to use Rich
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

console = Console()


class TerminalUI:
    """Handles all visual output to the terminal."""

    def display_report(self, report: AnalysisReport) -> None:
        """Render the analysis summary report."""
        table = Table(title="Analysis Summary", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="dim")
        table.add_column("Details")

        table.add_row("App URL", report.app_url)
        table.add_row("Supabase URL", report.supabase_url)
        table.add_row("Anon Key", f"[yellow]{report.anon_key[:48]}...[/yellow]")
        table.add_row("Auth Endpoints", str(report.auth_endpoints_count))
        table.add_row("REST Tables", str(report.rest_tables_count))
        table.add_row("RPC Calls", str(report.rpc_calls_count))
        table.add_row("Edge Functions", str(report.edge_functions_count))
        table.add_row("Bundle", f"{report.bundle_name} ({report.bundle_size_kb:.1f} KB)")

        console.print("\n")
        console.print(table)
        console.print(f"\n[bold green]Swagger saved to:[/bold green] {report.swagger_path}")

    def display_test_results(self, results: list[dict[str, Any]]) -> None:
        """Render a table with endpoint test results."""
        if not results:
            return

        table = Table(title="Endpoint Reliability Tests", show_header=True)
        table.add_column("Status", justify="center")
        table.add_column("Method")
        table.add_column("Path")
        table.add_column("Result")

        for r in results:
            status_style = "green" if r["accessible"] else "red"
            status_text = f"[{status_style}]{r['status']}[/{status_style}]"

            table.add_row(
                status_text,
                r["method"],
                r["path"],
                r["reason"] if r["reason"] else "[dim]OK[/dim]",
            )

        console.print("\n")
        console.print(table)

    def print_error(self, message: str) -> None:
        """Render an error message."""
        console.print(f"[bold red]ERROR:[/bold red] {message}")

    def print_info(self, message: str) -> None:
        """Render an info message."""
        console.print(f"[bold blue]INFO:[/bold blue] {message}")
