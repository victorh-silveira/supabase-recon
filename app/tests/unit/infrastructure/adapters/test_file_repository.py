"""Testes unitarios para o adaptador FileRepository."""

from pathlib import Path

import pytest

from infrastructure.adapters.file_repository import FileRepository


@pytest.fixture
def repo(tmp_path):
    """Retorna uma instancia de FileRepository apontada para um diretorio temporario."""
    return FileRepository(base_output_path=str(tmp_path))


@pytest.mark.unit
@pytest.mark.infrastructure
def test_get_project_dir(repo, tmp_path):
    """Testa criacao e nomenclatura do diretorio do projeto."""
    project_dir = repo.get_project_dir("myapp.com")
    assert project_dir == tmp_path / "myapp.com"
    assert project_dir.exists()


@pytest.mark.unit
@pytest.mark.infrastructure
def test_write_text(repo, tmp_path):
    """Testa gravacao de texto em arquivo."""
    file_path = tmp_path / "test.txt"
    repo.write_text(file_path, "content")
    assert file_path.read_text() == "content"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_find_largest_js(repo, tmp_path):
    """Testa busca pelo maior arquivo JS."""
    f1 = tmp_path / "small.js"
    f1.write_text("a")
    f2 = tmp_path / "large.js"
    f2.write_text("abc")

    largest = repo.find_largest_js(tmp_path)
    assert largest.name == "large.js"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_find_largest_js_none(repo, tmp_path):
    """Testa busca por JS quando nao ha nenhum arquivo."""
    assert repo.find_largest_js(tmp_path) is None


@pytest.mark.unit
@pytest.mark.infrastructure
def test_write_bytes(repo, tmp_path):
    """Testa gravacao de bytes em arquivo."""
    file_path = tmp_path / "test.bin"
    repo.write_bytes(file_path, b"content")
    assert file_path.read_bytes() == b"content"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_write_text_error_patch(repo, monkeypatch):
    """Testa tratamento de OSError em write_text usando monkeypatch."""

    def mock_write(*args, **kwargs):
        raise OSError("Disk full")

    monkeypatch.setattr("pathlib.Path.write_text", mock_write)
    repo.write_text(Path("any.txt"), "content")


@pytest.mark.unit
@pytest.mark.infrastructure
def test_write_bytes_error_patch(repo, monkeypatch):
    """Testa tratamento de OSError em write_bytes usando monkeypatch."""

    def mock_write(*args, **kwargs):
        raise OSError("Disk full")

    monkeypatch.setattr("pathlib.Path.write_bytes", mock_write)
    repo.write_bytes(Path("any.bin"), b"content")
