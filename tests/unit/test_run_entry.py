"""Ponto de entrada na raiz do repositório."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import recon.presentation.cli as cli_mod

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def test_run_py_main_calls_cli_main(monkeypatch) -> None:
    """run.main delega para recon.presentation.cli.main."""
    called: list[bool] = []

    def stub() -> None:
        called.append(True)

    monkeypatch.setattr(cli_mod, "main", stub)
    run_mod = importlib.import_module("run")
    run_mod.main()
    assert called == [True]
