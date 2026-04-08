"""Limpeza de caches, lint (isort/ruff), segurança, testes e coverage.

Por omissão o lint é só verificação (alinhado a execuções manuais e ao CI: não escreve ficheiros).
O hook ``clean-workspace`` do pre-commit invoca ``--fix-lint`` (isort, ``ruff check --fix``, ``ruff format``).
"""

from __future__ import annotations

import argparse
import os
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
    _print("\n[CLEAN] [1/5] caches")
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


def run_linting(*, apply_fixes: bool = False) -> None:
    """Executa isort e ruff; com ``apply_fixes`` aplica correções, senão só verifica (CI/pre-commit)."""
    mode = "aplicar correcoes" if apply_fixes else "apenas verificacao"
    _print(f"\n[CLEAN] [2/5] lint (isort/ruff) | {mode}")
    if apply_fixes:
        tools: tuple[tuple[str, list[str]], ...] = (
            ("Isort", ["isort", "."]),
            ("Ruff Check", ["ruff", "check", "--fix", "."]),
            ("Ruff Format", ["ruff", "format", "."]),
        )
    else:
        tools = (
            ("Isort", ["isort", "--check-only", "."]),
            ("Ruff Check", ["ruff", "check", "."]),
            ("Ruff Format", ["ruff", "format", "--check", "."]),
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
    _print("\n[CLEAN] [3/5] docs | interrogate")
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
    _print("\n[CLEAN] [4/5] segurança | bandit & pip-audit")
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


def run_tests_with_coverage(*, fail_under: float) -> None:
    """Executa pytest com coverage e falha abaixo do percentual mínimo."""
    _print("\n[CLEAN] [5/5] testes+coverage | pytest + coverage")
    run_cmd = [
        "python",
        "-m",
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests",
        "-q",
        "--tb=short",
    ]
    res_run = subprocess.run(run_cmd, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
    print(res_run.stdout)
    if res_run.stderr:
        print(res_run.stderr)
    if res_run.returncode != 0:
        _print("[CLEAN] erro | pytest/coverage")
        sys.exit(1)
    report_cmd = ["python", "-m", "coverage", "report", "-m", f"--fail-under={fail_under:.2f}"]
    res_report = subprocess.run(report_cmd, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
    print(res_report.stdout)
    if res_report.stderr:
        print(res_report.stderr)
    if res_report.returncode != 0:
        _print(f"[CLEAN] erro | coverage abaixo do minimo ({fail_under:.2f}%)")
        sys.exit(1)
    _print(f"[CLEAN] ok | coverage >= {fail_under:.2f}%")


def run_pytest_only() -> None:
    """Executa suíte de testes sem coverage."""
    _print("\n[CLEAN] [5/5] testes | pytest")
    run_cmd = ["python", "-m", "pytest", "tests", "-q", "--tb=short"]
    res = subprocess.run(run_cmd, capture_output=True, text=True, encoding="utf-8", check=False)  # noqa: S603
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    if res.returncode != 0:
        _print("[CLEAN] erro | pytest")
        sys.exit(1)
    _print("[CLEAN] ok | pytest")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Limpeza, lint, docs e auditoria de segurança.")
    parser.add_argument(
        "--fix-lint",
        action="store_true",
        help="Aplica isort/ruff no disco (sem isto: só verificação, compatível com pre-commit).",
    )
    parser.add_argument(
        "--stage",
        choices=("all", "lint", "security", "pytest", "test"),
        default="all",
        help="Executa apenas uma etapa (lint, security, pytest, test) ou fluxo completo (all).",
    )
    parser.add_argument(
        "--with-coverage",
        action="store_true",
        help="Executa pytest com coverage e aplica fail-under configurado.",
    )
    parser.add_argument(
        "--coverage-fail-under",
        type=float,
        default=float(os.getenv("AETHER_COVERAGE_FAIL_UNDER", "100")),
        help="Percentual mínimo de cobertura para aprovação (default: env AETHER_COVERAGE_FAIL_UNDER ou 100).",
    )
    args = parser.parse_args()
    setup_utf8()
    _print("=" * 75)
    _print("[CLEAN] supabase-recon")
    _print(f"[CLEAN] cwd={Path.cwd()}")
    _print("=" * 75)
    clean_caches()
    stage = str(args.stage)
    if stage == "all":
        run_linting(apply_fixes=args.fix_lint)
        run_interrogate()
        run_pytest_only()
        if args.with_coverage:
            run_tests_with_coverage(fail_under=max(0.0, min(100.0, float(args.coverage_fail_under))))
        run_security_audit()
    elif stage == "lint":
        run_linting(apply_fixes=args.fix_lint)
        run_interrogate()
    elif stage == "security":
        run_security_audit()
    elif stage == "pytest":
        run_pytest_only()
    elif stage == "test":
        run_tests_with_coverage(fail_under=max(0.0, min(100.0, float(args.coverage_fail_under))))
    _print("\n" + "=" * 75)
    _print("[CLEAN] fim")
    _print("=" * 75)
