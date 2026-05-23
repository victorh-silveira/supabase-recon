"""Asset models for discovered application files."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Asset:
    """Represents a static asset (JS, CSS, etc.) to be downloaded or analyzed."""

    url_path: str
    local_path: Path | None = None
    size_bytes: int = 0

    @property
    def is_js(self) -> bool:
        """Check if the asset is a JavaScript file."""
        return self.url_path.endswith(".js")

    @property
    def filename(self) -> str:
        """Return the filename from the url path."""
        return Path(self.url_path).name
