"""Contrato de download de assets."""

from pathlib import Path
from typing import Protocol

from domain.entities.asset import Asset


class AssetDownloaderPort(Protocol):
    """Port for downloading application assets."""

    def download_all(self, base_url: str, assets: list[Asset], project_dir: Path) -> list[Path]:
        """Download assets from a base URL into a project directory."""
        ...
