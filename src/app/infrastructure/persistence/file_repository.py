"""Repository for managing physical file storage."""

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


class FileRepository:
    """Handles directory creation and file persistence."""

    def __init__(self, base_output_path: str = "output"):
        """Initialize with a base directory (default is 'output')."""
        self.base_path = Path(base_output_path)

    def get_project_dir(self, domain: str) -> Path:
        """Get the specific directory for a project domain."""
        # Sanitize domain name for folder creation
        safe_domain = domain.replace(":", "_").replace("/", "_")
        project_dir = self.base_path / safe_domain
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def write_text(self, file_path: Path, content: str) -> None:
        """Write text content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"Saved: {file_path}")
        except OSError as e:
            logger.error(f"Failed to write text to {file_path}: {e}")

    def write_bytes(self, file_path: Path, content: bytes) -> None:
        """Write binary content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(content)
            logger.info(f"Saved: {file_path}")
        except OSError as e:
            logger.error(f"Failed to write bytes to {file_path}: {e}")

    def find_largest_js(self, directory: Path) -> Path | None:
        """Find the largest .js file within a directory (main bundle heuristic)."""
        js_files = list(directory.rglob("*.js"))
        if not js_files:
            return None
        return max(js_files, key=lambda p: p.stat().st_size if p.exists() else 0)
