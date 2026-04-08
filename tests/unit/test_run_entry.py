"""Ponto de entrada na raiz do repositório."""

from __future__ import annotations

import importlib
import runpy
import sys
from pathlib import Path


def test_run_py_main_calls_cli_main(monkeypatch) -> None:
    """run.main delega para recon.presentation.cli.main."""
    run_mod = importlib.import_module("run")
    called: list[bool] = []

    def stub(*_args, **_kwargs) -> None:
        called.append(True)

    monkeypatch.setattr("recon.presentation.cli.main", stub)
    run_mod.main()
    assert called == [True]


def test_run_py_dunder_main_executes_entrypoint(monkeypatch) -> None:
    """Execução via __main__ dispara o mesmo ponto de entrada."""
    called: list[bool] = []

    def stub(*_args, **_kwargs) -> None:
        called.append(True)

    monkeypatch.setattr("recon.presentation.cli.main", stub)
    runpy.run_path(str(Path(__file__).resolve().parents[2] / "run.py"), run_name="__main__")
    assert called == [True]


def test_run_module_inserts_src_in_sys_path_when_missing() -> None:
    """Ao importar run.py, adiciona `src/` no sys.path quando ausente."""
    run_mod = importlib.import_module("run")
    src = str(Path(run_mod.__file__).resolve().parent / "src")
    while src in sys.path:
        sys.path.remove(src)
    importlib.reload(run_mod)
    assert src in sys.path
