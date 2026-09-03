from __future__ import annotations

import json
import sys
from collections.abc import Iterable
from pathlib import Path

import yaml
from gate_runtime import REPO_ROOT, exit_if_violations, fail, run_command


SKIP_YAML_PARTS = {".venv", "venv", "node_modules", "templates"}


def _iter_yaml_files() -> list[Path]:
    found: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".yml", ".yaml"}:
            continue
        if any(part in SKIP_YAML_PARTS for part in path.parts):
            continue
        found.append(path)
    extra = REPO_ROOT / ".pre-commit-config.yaml"
    if extra.is_file() and extra not in found:
        found.append(extra)
    return sorted(found)


def _iter_json_files() -> list[Path]:
    return [
        REPO_ROOT / "linters" / "releaserc.json",
        REPO_ROOT / ".vscode" / "settings.json",
    ]


def _missing(paths: Iterable[Path]) -> list[str]:
    return [str(path) for path in paths if not path.is_file()]


def stage_yaml_lint() -> None:
    files = _iter_yaml_files()
    if not files:
        fail("[ERRO] Nenhum YAML encontrado para lint")
    run_command(
        [sys.executable, "-m", "yamllint", *[str(path) for path in files]],
        "YAML Lint",
        cwd=REPO_ROOT,
    )


def stage_yaml_validate() -> None:
    violations: list[str] = []
    for path in _iter_yaml_files():
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            violations.append(f"{path}: {exc}")
    exit_if_violations("YAML invalido (safe_load):", violations)
    print("[OK] YAML validado com yaml.safe_load.")


def stage_json_lint() -> None:
    missing = _missing(_iter_json_files())
    exit_if_violations("JSON ausente:", missing)
    violations: list[str] = []
    for path in _iter_json_files():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(f"{path}: {exc}")
    exit_if_violations("JSON invalido:", violations)
    print("[OK] JSON parseado.")


def stage_json_validate() -> None:
    stage_json_lint()
    releaserc = json.loads((REPO_ROOT / "linters" / "releaserc.json").read_text(encoding="utf-8"))
    settings = json.loads((REPO_ROOT / ".vscode" / "settings.json").read_text(encoding="utf-8"))
    violations: list[str] = []
    if not isinstance(releaserc, dict) or "branches" not in releaserc or "plugins" not in releaserc:
        violations.append("linters/releaserc.json sem branches/plugins")
    if not isinstance(settings, dict):
        violations.append(".vscode/settings.json nao e objeto")
    exit_if_violations("JSON invalido estruturalmente:", violations)
    print("[OK] JSON estruturalmente valido.")
