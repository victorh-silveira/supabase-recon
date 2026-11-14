"""Contrato de persistencia em disco."""

from pathlib import Path
from typing import Protocol


class FileRepositoryPort(Protocol):
    """Porta para operacoes locais de arquivos e diretorios."""

    def get_project_dir(self, domain: str) -> Path:
        """Retorna o diretorio do projeto para um dominio, criando-o se necessario."""
        ...

    def write_text(self, file_path: Path, content: str) -> None:
        """Grava conteudo textual em um arquivo."""
        ...

    def write_bytes(self, file_path: Path, content: bytes) -> None:
        """Grava conteudo binario em um arquivo."""
        ...

    def find_largest_js(self, directory: Path) -> Path | None:
        """Localiza o maior arquivo JavaScript dentro de um diretorio."""
        ...
