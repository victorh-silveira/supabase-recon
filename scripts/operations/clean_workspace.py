"""Limpeza de caches, lint (isort/ruff), interrogate, segurança (bandit/pip-audit)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from contextlib import suppress
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _print(msg: str) -> None:
    """Imprime uma linha no stdout com flush imediato."""
    print(msg, flush=True)


def setup_utf8() -> None:
    """Configura stdout/stderr em UTF-8 no Windows."""
    if sys.platform == "win32":
        with suppress(OSError, AttributeError):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")


def clean_caches() -> None:
    """Remove .pytest_cache, .ruff_cache, __pycache__, build, dist."""
    _print("\n[CLEAN] [1/4] caches")
    removed = 0
    patterns = (".pytest_cache", ".ruff_cache", "*.egg-info", "__pycache__", "build", "dist")
    base_path = Path.cwd()
    for p in base_path.rglob("*"):
        if any(p.match(pat) for pat in patterns):
            with suppress(OSError):
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                removed += 1
    _print(f"[CLEAN] ok | removidos={removed}")


def run_linting() -> None:
    """Executa isort, ruff check --fix e ruff format; sai com 1 se algum falhar."""
    _print("\n[CLEAN] [2/4] lint (isort/ruff)")
    tools: tuple[tuple[str, list[str]], ...] = (
        ("Isort", ["isort", "."]),
        ("Ruff Check", ["ruff", "check", "--fix", "."]),
        ("Ruff Format", ["ruff", "format", "."]),
    )
    failed = False
    for name, cmd in tools:
        _print(f"[CLEAN] roda | {name}")
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
        if res.returncode != 0:
            _print(f"[CLEAN] erro | {name}")
            print(res.stdout)
            print(res.stderr)
            failed = True
        else:
            _print(f"[CLEAN] ok | {name}")
    if failed:
        _print("\n[CLEAN] erro | padroes nao atendidos")
        sys.exit(1)
    _print("[CLEAN] ok | lint concluido")


def run_interrogate() -> None:
    """Roda interrogate conforme pyproject (fail-under)."""
    _print("\n[CLEAN] [3/4] docs | interrogate")
    try:
        cmd = ["interrogate", "-v", "--fail-under", "100", "."]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
        print(res.stdout)
        if res.returncode != 0:
            _print("[CLEAN] erro | interrogate abaixo do minimo")
            sys.exit(1)
    except (subprocess.SubprocessError, OSError) as e:
        _print("[CLEAN] erro | interrogate")
        _print(f"[CLEAN] detalhe={e}")
        sys.exit(1)


def run_security_audit() -> None:
    """Bandit e pip-audit; falha o processo se algum reportar problema (alinhado ao CI)."""
    _print("\n[CLEAN] [4/4] segurança | bandit & pip-audit")
    _print("[CLEAN] roda | Bandit")
    cmd_bandit = [
        "bandit",
        "-r",
        ".",
        "-ll",
        "-ii",
        "-c",
        "pyproject.toml",
        "-x",
        "./tests,./venv,./.venv,./build,./dist,./output",
    ]
    res = subprocess.run(cmd_bandit, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    if res.returncode != 0:
        _print("[CLEAN] erro | Bandit")
        sys.exit(1)
    _print("[CLEAN] ok | Bandit")

    _print("[CLEAN] roda | pip-audit")
    for req_name in ("requirements.txt", "requirements-dev.txt"):
        req = Path(req_name)
        if not req.exists():
            continue
        cmd = ["pip-audit", "-r", str(req)]
        if req.name == "requirements-dev.txt":
            cmd.extend(["--ignore-vuln", "PYSEC-2022-42969"])
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
        print(res.stdout)
        if res.stderr:
            print(res.stderr)
        if res.returncode != 0:
            _print(f"[CLEAN] erro | pip-audit em {req_name}")
            sys.exit(1)
        _print(f"[CLEAN] ok | pip-audit {req_name}")


if __name__ == "__main__":
    setup_utf8()
    _print("=" * 75)
    _print("[CLEAN] supabase-recon")
    _print(f"[CLEAN] cwd={Path.cwd()}")
    _print("=" * 75)
    clean_caches()
    run_linting()
    run_interrogate()
    run_security_audit()
    _print("\n" + "=" * 75)
    _print("[CLEAN] fim")
    _print("=" * 75)
