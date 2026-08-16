import argparse
import ast
import os
import shutil
import subprocess
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = APP_ROOT.parent
SRC_ROOT = APP_ROOT / "src"

FORBIDDEN_IMPORTS = {
    "domain": {"infrastructure", "presentation", "application"},
    "application": {"infrastructure", "presentation"},
}


def _use_app_cwd() -> None:
    os.chdir(APP_ROOT)


def run_tool(module, args, description):
    print(f"\n>>> Executando: {description}")
    command = [sys.executable, "-m", module] + args
    print(f"Command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro durante {description}: {e}")
        sys.exit(e.returncode)


def _module_root(module_name: str) -> str | None:
    top = module_name.split(".", 1)[0]
    if top in {"domain", "application", "infrastructure", "presentation"}:
        return top
    return None


def stage_layer_dependencies() -> None:
    print("\n>>> Executando: Verificacao de dependencias entre camadas")
    violations: list[str] = []

    for path in SRC_ROOT.rglob("*.py"):
        relative = path.relative_to(SRC_ROOT)
        if not relative.parts:
            continue
        layer = relative.parts[0]
        if layer not in FORBIDDEN_IMPORTS:
            continue

        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            imported: list[str] = []
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported = [node.module]

            for name in imported:
                target = _module_root(name)
                if target and target in FORBIDDEN_IMPORTS[layer]:
                    violations.append(f"{path}: {layer} importa {name}")

    if violations:
        print("\n[ERRO] Violacao de dependencias entre camadas:")
        for item in violations:
            print(f"  - {item}")
        sys.exit(1)
    print("[OK] Regras de dependencia entre camadas respeitadas.")


def stage_lint():
    print("\n>>> Executando: Ruff Check (auto-fix)")
    fix_cmd = [sys.executable, "-m", "ruff", "check", "--fix", "."]
    print(f"Command: {' '.join(fix_cmd)}")
    subprocess.run(fix_cmd, check=True, text=True)
    run_tool("ruff", ["check", "."], "Ruff Check")
    run_tool("ruff", ["format", "."], "Ruff Format")
    run_tool("interrogate", ["-vv", "src"], "Interrogate Docstrings")
    run_tool("vulture", [], "Vulture Dead Code Detection")
    run_tool("mypy", ["--config-file", "pyproject.toml"], "Mypy Strict")
    stage_layer_dependencies()
    stage_structure()


def stage_structure(max_lines=300):
    print(f"\n>>> Executando: Verificacao Estrutural (Max {max_lines} linhas)")
    violations = []

    for path in APP_ROOT.rglob("*.py"):
        if ".venv" in path.parts or "venv" in path.parts or ".git" in path.parts:
            continue

        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            count = len(lines)
            if count > max_lines:
                violations.append(f"{path}: {count} linhas")

    if violations:
        print("\n[ERRO] Violacao de limite de linhas encontrada:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    print(f"[OK] Todos os arquivos estao abaixo de {max_lines} linhas.")


def stage_test(fail_under=100):
    run_tool("coverage", ["run", "--branch", "-m", "pytest"], "Pytest execution (branch coverage)")
    run_tool("coverage", ["report", f"--fail-under={fail_under}"], f"Coverage report (min {fail_under}%)")


def stage_security():
    ignored_vulns = ["PYSEC-2022-42969", "CVE-2026-45409"]
    ignore_args = []
    for vuln in ignored_vulns:
        ignore_args.extend(["--ignore-vuln", vuln])

    run_tool("bandit", ["-r", "src", "-c", "pyproject.toml"], "Bandit Security Scan")
    run_tool("pip_audit", ignore_args, "Pip-audit Vulnerability Scan")


def stage_clean():
    print("\n>>> Running: Limpeza de lixo e caches")

    def safe_remove(p: Path):
        try:
            if p.is_dir():
                shutil.rmtree(p)
                print(f"Removido diretorio: {p}")
            else:
                p.unlink()
                print(f"Removido arquivo: {p}")
        except Exception as e:
            print(f"Erro ao remover {p}: {e}")

    for scan_root in (APP_ROOT, REPO_ROOT):
        for path in scan_root.rglob("__pycache__"):
            if path.is_dir():
                safe_remove(path)

        for ext in ("*.pyc", "*.pyo", "*.pyd"):
            for path in scan_root.rglob(ext):
                if path.is_file():
                    safe_remove(path)

    for name in (".pytest_cache", ".ruff_cache", ".coverage", "htmlcov", "dist", "build", ".mypy_cache"):
        p = APP_ROOT / name
        if p.exists():
            safe_remove(p)

    for name in ("data", "logs"):
        p = REPO_ROOT / name
        if p.exists():
            safe_remove(p)


def main():
    parser = argparse.ArgumentParser(description="Supabase Recon Quality Gate")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["lint", "pytest", "security", "test", "clean"],
        help="Stage to execute",
    )
    parser.add_argument("--coverage-fail-under", type=int, default=100, help="Minimum coverage percentage")

    args = parser.parse_args()
    _use_app_cwd()

    if args.stage == "lint":
        stage_lint()
    elif args.stage in ["pytest", "test"]:
        stage_test(args.coverage_fail_under)
    elif args.stage == "security":
        stage_security()
    elif args.stage == "clean":
        stage_clean()

    print("\n[SUCESSO] Estagio concluido com sucesso.")


if __name__ == "__main__":
    main()
