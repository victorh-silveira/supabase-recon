"""Repository adapter for managing physical file storage."""

from __future__ import annotations

import logging
from pathlib import Path

from infrastructure.logging.events import log_event


logger = logging.getLogger(__name__)


class FileRepository:
    """Handles directory creation and file persistence."""

    def __init__(self, base_output_path: str = "output") -> None:
        """Initialize with a base directory (default is 'output')."""
        self.base_path = Path(base_output_path)

    def get_project_dir(self, domain: str) -> Path:
        """Get the specific directory for a project domain."""
        safe_domain = domain.replace(":", "_").replace("/", "_")
        project_dir = self.base_path / safe_domain
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def write_text(self, file_path: Path, content: str) -> None:
        """Write text content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            log_event(logger, logging.DEBUG, "recon.file.write_text.ok", path=str(file_path))
        except OSError as e:
            log_event(
                logger,
                logging.ERROR,
                "recon.file.write_text.failed",
                path=str(file_path),
                error=str(e),
            )

    def write_bytes(self, file_path: Path, content: bytes) -> None:
        """Write binary content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(content)
            log_event(logger, logging.DEBUG, "recon.file.write_bytes.ok", path=str(file_path))
        except OSError as e:
            log_event(
                logger,
                logging.ERROR,
                "recon.file.write_bytes.failed",
                path=str(file_path),
                error=str(e),
            )

    def find_largest_js(self, directory: Path) -> Path | None:
        """Find the largest .js file within a directory (main bundle heuristic)."""
        js_files = list(directory.rglob("*.js"))
        if not js_files:
            return None
        return max(js_files, key=lambda p: p.stat().st_size if p.exists() else 0)
