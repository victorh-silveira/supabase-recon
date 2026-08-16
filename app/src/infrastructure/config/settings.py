"""Carrega Settings a partir de variaveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    http_timeout_seconds: int
    output_base_path: str
    log_level: str

    @classmethod
    def from_env(cls, repo_root: Path) -> Settings:
        """Load settings from .env (unless disabled) and process environment."""
        if os.environ.get("RECON_DISABLE_DOTENV", "").lower() not in {"1", "true", "yes"}:
            env_path = repo_root / ".env"
            if env_path.exists():
                load_dotenv(env_path, override=False)

        timeout_raw = os.environ.get("RECON_HTTP_TIMEOUT_SECONDS", "30")
        output_path = os.environ.get("RECON_OUTPUT_BASE_PATH", "output")
        log_level = os.environ.get("RECON_LOG_LEVEL", "INFO").upper()

        try:
            timeout = int(timeout_raw)
        except ValueError:
            timeout = 30

        return cls(
            http_timeout_seconds=timeout,
            output_base_path=output_path,
            log_level=log_level,
        )
