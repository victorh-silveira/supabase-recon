"""Cobertura das utilidades definidas em tests/conftest.py."""

from __future__ import annotations

from pathlib import Path

from tests.conftest import pytest_collection_modifyitems


class _FakeItem:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.markers: list[object] = []

    def add_marker(self, marker: object) -> None:
        self.markers.append(marker)


def test_collection_modifyitems_marks_unit_when_path_has_tests_unit() -> None:
    """Marca item como unit quando o caminho contém `tests/unit`."""
    item = _FakeItem("tests/unit/x_test.py")
    pytest_collection_modifyitems(config=None, items=[item])  # type: ignore[arg-type]
    assert len(item.markers) == 1


def test_collection_modifyitems_handles_paths_outside_tests() -> None:
    """Não adiciona marcador unit para caminhos fora da pasta tests."""
    item = _FakeItem("src/recon/app.py")
    pytest_collection_modifyitems(config=None, items=[item])  # type: ignore[arg-type]
    assert item.markers == []
