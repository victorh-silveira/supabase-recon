"""Garante que a matriz agent-coverage aponta para arquivos existentes e valida o harness canônico genérico."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
MATRIX = REPO_ROOT / "docs" / "agent-coverage.md"
AGENTS_DIR = REPO_ROOT / ".agents"
RULES_DIR = AGENTS_DIR / "rules"
SKILLS_DIR = AGENTS_DIR / "skills"
MCP_CONFIG = AGENTS_DIR / "mcp.json"


@pytest.mark.unit
def test_agent_coverage_matrix_files_exist():
    """Rules e skills referenciadas na matriz devem existir no disco sob .agents/."""
    text = MATRIX.read_text(encoding="utf-8")
    rules = set(re.findall(r"`(recon-[a-z0-9-]+\.mdc)`", text))
    skills = set(re.findall(r"`(recon-[a-z0-9-]+)`", text))
    skills = {name for name in skills if not name.endswith(".mdc")}

    assert rules, "matriz deve listar rules"
    assert skills, "matriz deve listar skills"

    missing_rules = sorted(name for name in rules if not (RULES_DIR / name).is_file())
    missing_skills = sorted(name for name in skills if not (SKILLS_DIR / name / "SKILL.md").is_file())

    assert not missing_rules, f"rules ausentes: {missing_rules}"
    assert not missing_skills, f"skills ausentes: {missing_skills}"


@pytest.mark.unit
def test_all_agent_rules_are_always_apply_true():
    """Toda rule versionada em .agents/rules deve declarar alwaysApply true."""
    files = sorted(RULES_DIR.glob("*.mdc"))
    assert files, "deve haver rules em .agents/rules"
    for path in files:
        content = path.read_text(encoding="utf-8")
        assert "alwaysApply: true" in content, f"{path.name} sem alwaysApply: true"


@pytest.mark.unit
def test_all_skill_directories_have_skill_md():
    """Cada pasta em .agents/skills deve conter SKILL.md."""
    dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    assert dirs, "deve haver skills em .agents/skills"
    for path in dirs:
        assert (path / "SKILL.md").is_file(), f"faltando SKILL.md em {path.name}"


@pytest.mark.unit
def test_mcp_config_exists_and_is_valid_json():
    """Manifesto .agents/mcp.json deve existir e conter JSON valido."""
    assert MCP_CONFIG.is_file(), "arquivo .agents/mcp.json deve existir"
    data = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "mcp.json deve ser um objeto JSON"
    assert "mcpServers" in data, "mcp.json deve conter chave mcpServers"
