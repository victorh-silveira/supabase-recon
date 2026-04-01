"""Configuração central de structlog (JSON ou consola legível)."""

from __future__ import annotations

import logging
import os
import sys

import structlog


def configure_logging(*, json_logs: bool | None = None) -> None:
    """Configura processadores structlog.

    Se `json_logs` for None, ativa JSON quando `RECON_LOG_JSON` é 1/true/yes.
    """
    if json_logs is None:
        json_logs = os.environ.get("RECON_LOG_JSON", "").strip().lower() in ("1", "true", "yes")

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    shared_pre = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        timestamper,
    ]

    if json_logs:
        processors = [
            *shared_pre,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = [
            *shared_pre,
            structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty()),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", stream=sys.stderr, level=logging.INFO)
