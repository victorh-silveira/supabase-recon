from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from clean_workspace import _dispatch
from config_gates import (
    _iter_json_files,
    _iter_yaml_files,
    stage_json_lint,
    stage_json_validate,
    stage_yaml_lint,
    stage_yaml_validate,
)
from gate_runtime import AREA_STAGES
from python_gates import _module_root, stage_lint, stage_validate


@pytest.mark.unit
def test_python_lint_and_validate_include_yaml_json():
    with (
        patch("python_gates.subprocess.run"),
        patch("python_gates.run_tool"),
        patch("python_gates.stage_yaml_lint") as yaml_lint,
        patch("python_gates.stage_json_lint") as json_lint,
        patch("python_gates.stage_yaml_validate") as yaml_validate,
        patch("python_gates.stage_json_validate") as json_validate,
        patch("python_gates.stage_layer_dependencies"),
        patch("python_gates.stage_structure"),
    ):
        stage_lint()
        stage_validate()
    yaml_lint.assert_called_once()
    json_lint.assert_called_once()
    yaml_validate.assert_called_once()
    json_validate.assert_called_once()


@pytest.mark.unit
def test_python_area_includes_crash_first_stages():
    stages = AREA_STAGES["python"]
    assert {"lint", "validate", "security", "test", "build"}.issubset(stages)
    assert list(AREA_STAGES) == ["python"]


@pytest.mark.unit
def test_dispatch_rejects_unknown_area_and_stage():
    with pytest.raises(SystemExit) as unknown_area:
        _dispatch("yaml", "lint", 100)
    assert unknown_area.value.code == 1
    with pytest.raises(SystemExit) as unknown_stage:
        _dispatch("python", "nope", 100)
    assert unknown_stage.value.code == 1


@pytest.mark.unit
def test_dispatch_python_stages():
    calls: list[str] = []

    def mark(name: str) -> MagicMock:
        return MagicMock(side_effect=lambda *_args, **_kwargs: calls.append(name))

    with (
        patch("clean_workspace.stage_lint", mark("py_lint")),
        patch("clean_workspace.stage_validate", mark("py_validate")),
        patch("clean_workspace.stage_security", mark("py_security")),
        patch("clean_workspace.stage_test", mark("py_test")),
        patch("clean_workspace.stage_build", mark("py_build")),
        patch("clean_workspace.stage_clean", mark("clean")),
    ):
        _dispatch("python", "lint", 100)
        _dispatch("python", "security", 100)
        _dispatch("python", "test", 90)
        _dispatch("python", "pytest", 90)
        _dispatch("python", "validate", 100)
        _dispatch("python", "build", 100)
        _dispatch("python", "clean", 100)
    assert calls == [
        "py_lint",
        "py_security",
        "py_test",
        "py_test",
        "py_validate",
        "py_build",
        "clean",
    ]


@pytest.mark.unit
def test_iter_yaml_skips_templates_and_finds_workflows():
    paths = {path.as_posix() for path in _iter_yaml_files()}
    assert any("workflows/ci.yml" in item for item in paths)
    assert all("templates" not in item for item in paths)


@pytest.mark.unit
def test_iter_json_includes_releaserc_and_vscode():
    names = [path.name for path in _iter_json_files()]
    assert "releaserc.json" in names
    assert "settings.json" in names


@pytest.mark.unit
def test_module_root_layers():
    assert _module_root("domain.entities.asset") == "domain"
    assert _module_root("application.ports.http_client") == "application"
    assert _module_root("json") is None


@pytest.mark.unit
def test_json_and_yaml_validate_current_repo():
    stage_json_validate()
    stage_yaml_validate()


@pytest.mark.unit
def test_yaml_lint_fails_without_files():
    with patch("config_gates._iter_yaml_files", return_value=[]), pytest.raises(SystemExit) as exc:
        stage_yaml_lint()
    assert exc.value.code == 1


@pytest.mark.unit
def test_json_lint_fails_when_missing():
    with patch("config_gates._iter_json_files", return_value=[Path("/no/such.json")]), pytest.raises(SystemExit) as exc:
        stage_json_lint()
    assert exc.value.code == 1
