"""Argumentos, logging e composição do caso de uso."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import structlog

from recon.application.recon_orchestrator import ReconOptions
from recon.domain.exceptions import BundleNotFoundError, MissingAnonKeyError
from recon.infrastructure.logging_config import configure_logging
from recon.presentation.human_report import emit_human_summary
from recon.wiring import build_orchestrator


def _env_truthy(name: str) -> bool:
    """Devolve True se a variável de ambiente for 1/true/yes (case-insensitive)."""
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes")


def build_parser() -> argparse.ArgumentParser:
    """Constrói o ArgumentParser com todas as flags do recon."""
    parser = argparse.ArgumentParser(
        description="Analisa app Lovable/Supabase, gera swagger.yaml e (opcionalmente) sonda endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run.py --url https://application.lovable.app\n"
            "  python run.py --url https://application.lovable.app --skip-download\n"
            "  python run.py --url https://application.lovable.app --skip-download --no-test\n"
            "  python run.py --url https://application.lovable.app --skip-download --methods get\n"
            "\n"
            "Logs estruturados em stderr (nível INFO).\n"
            "- RECON_LOG_JSON=1  → uma linha JSON por evento.\n"
            "- --human-summary ou RECON_HUMAN_SUMMARY=1  → também imprime tabela legível em stderr.\n"
        ),
    )
    parser.add_argument("--url", required=True, help="URL da app")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reutiliza assets em output/<host>/ se existirem",
    )
    parser.add_argument("--no-test", action="store_true", help="Não sondar endpoints após gerar OpenAPI")
    parser.add_argument(
        "--methods",
        default="get,post",
        help="Métodos HTTP a usar na sonda (default: get,post)",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="Pasta raiz para output/ (default: ./output)",
    )
    parser.add_argument(
        "--human-summary",
        action="store_true",
        help="Além dos logs estruturados, envia resumo tabular legível para stderr",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Ponto de entrada do programa."""
    configure_logging()
    log = structlog.get_logger()

    parser = build_parser()
    args = parser.parse_args(argv)

    human = bool(args.human_summary) or _env_truthy("RECON_HUMAN_SUMMARY")

    log.info("recon.cli.start", app_url=args.url, human_summary_sink=human)

    probe_methods = frozenset(m.strip().lower() for m in args.methods.split(","))
    options = ReconOptions(
        app_url=args.url,
        skip_download_if_existing=bool(args.skip_download),
        run_endpoint_probe=not args.no_test,
        probe_methods=probe_methods,
    )

    orchestrator = build_orchestrator(log=log)

    try:
        analysis = orchestrator.run(options, output_root=args.output_root)
    except (MissingAnonKeyError, BundleNotFoundError) as e:
        log.error("recon.pipeline.domain_error", error=str(e))
        raise SystemExit(1) from e

    log.info(
        "recon.pipeline.done",
        supabase_url=analysis.supabase.base_url,
        event_followup="recon.cli.summary",
    )
    log.info(
        "recon.cli.summary",
        app_url=args.url.rstrip("/"),
        supabase_url=analysis.supabase.base_url,
        anon_key_prefix=analysis.supabase.anon_key[:48],
        anon_key_length=len(analysis.supabase.anon_key),
        auth_endpoints=len(analysis.auth_endpoints),
        rest_tables=len(analysis.tables),
        rpc_calls=len(analysis.rpcs),
        edge_functions=len(analysis.edge_functions),
    )

    if human:
        emit_human_summary(analysis=analysis, app_url=args.url)
