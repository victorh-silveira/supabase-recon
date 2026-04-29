"""Workspace quality and cleanup script for CI/CD pipelines.

This script acts as a bridge between GitHub Actions and the various quality
tools (Ruff, Pytest, Interrogate, etc.) to ensure consistency with the
local development environment.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Executes a shell command and prints its output."""
    print(f"\n>>> Running: {description}")
    print(f"Command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, text=True)  # noqa: S603
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e}")
        sys.exit(e.returncode)


def stage_lint():
    """Runs linting and docstring checks."""
    run_command(["ruff", "check", "--fix", "--exit-non-zero-on-fix", "."], "Ruff Check")
    run_command(["ruff", "format", "."], "Ruff Format")
    run_command(["interrogate", "-vv", "."], "Interrogate Docstrings")


def stage_test(fail_under=100):
    """Runs unit tests and coverage verification."""
    run_command(["python", "-m", "coverage", "run", "-m", "pytest"], "Pytest execution")
    run_command(
        ["python", "-m", "coverage", "report", f"--fail-under={fail_under}"], f"Coverage report (min {fail_under}%)"
    )


def stage_security():
    """Runs static security analysis and dependency auditing."""
    ignored_vulns = ["PYSEC-2022-42969"]
    ignore_args = []
    for vuln in ignored_vulns:
        ignore_args.extend(["--ignore-vuln", vuln])

    run_command(["bandit", "-r", "src/", "-c", "pyproject.toml"], "Bandit Security Scan")
    run_command(["pip-audit", *ignore_args], "Pip-audit Vulnerability Scan")


def stage_clean():
    """Removes build artifacts, caches, and temporary files."""
    print("\n>>> Running: Limpeza de lixo e caches")
    root = Path()
    targets = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        ".pytest_cache",
        ".ruff_cache",
        ".coverage",
        "htmlcov",
        "data",
        "logs",
        "dist",
        "build",
    ]

    for pattern in targets:
        for path in root.glob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"Removido diretório: {path}")
                else:
                    path.unlink()
                    print(f"Removido arquivo: {path}")
            except Exception as e:  # noqa: BLE001
                print(f"Erro ao remover {path}: {e}")


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(description="Aether Engine Quality Gate")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["lint", "pytest", "security", "test", "clean"],
        help="Stage to execute",
    )
    parser.add_argument("--coverage-fail-under", type=int, default=100, help="Minimum coverage percentage")

    args = parser.parse_args()

    if args.stage == "lint":
        stage_lint()
    elif args.stage in ["pytest", "test"]:
        stage_test(args.coverage_fail_under)
    elif args.stage == "security":
        stage_security()
    elif args.stage == "clean":
        stage_clean()

    print("\n[SUCCESS] Stage completed successfully.")


if __name__ == "__main__":
    main()
