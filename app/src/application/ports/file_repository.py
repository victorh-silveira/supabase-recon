"""Contrato de persistencia em disco."""

from pathlib import Path
from typing import Protocol


class FileRepositoryPort(Protocol):
    """Port for local file and directory operations."""

    def get_project_dir(self, domain: str) -> Path:
        """Return the project directory for a domain, creating it if needed."""
        ...

    def write_text(self, file_path: Path, content: str) -> None:
        """Write text content to a file."""
        ...

    def write_bytes(self, file_path: Path, content: bytes) -> None:
        """Write binary content to a file."""
        ...

    def find_largest_js(self, directory: Path) -> Path | None:
        """Find the largest JavaScript file under a directory."""
        ...
