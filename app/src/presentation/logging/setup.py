"""Configuracao de logging da apresentacao."""

from __future__ import annotations

import logging

from rich.logging import RichHandler


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging with Rich and quiet HTTP client loggers."""
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = RichHandler(rich_tracebacks=True, show_path=False)
    handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    root.addHandler(handler)

    for name in ("urllib3", "requests", "urllib3.connectionpool"):
        logging.getLogger(name).setLevel(logging.WARNING)
