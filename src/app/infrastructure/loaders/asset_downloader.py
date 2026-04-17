"""Service for orchestrating asset downloads."""

import logging
from pathlib import Path

from app.domain.models.asset import Asset
from app.infrastructure.network.http_client import HTTPClient
from app.infrastructure.persistence.file_repository import FileRepository


logger = logging.getLogger(__name__)


class AssetDownloader:
    """Orchestrates downloading a list of assets to the local repository."""

    def __init__(self, http_client: HTTPClient, file_repository: FileRepository):
        """Initialize with network and persistence dependencies."""
        self.http_client = http_client
        self.file_repository = file_repository

    def download_all(self, base_url: str, assets: list[Asset], project_dir: Path) -> list[Path]:
        """Download a list of assets from a base URL to a project directory."""
        downloaded_paths = []

        logger.info(f"Downloading {len(assets)} assets to {project_dir}...")

        for asset in assets:
            # Construct full remote URL
            full_url = f"{base_url.rstrip('/')}/{asset.url_path.lstrip('/')}"

            # Construct local path (preserving folder structure)
            relative_path = asset.url_path.lstrip("/").replace("/", "\\")
            local_path = project_dir / relative_path

            # Download content
            try:
                data = self.http_client.get_bytes(full_url)
                if data is not None:
                    self.file_repository.write_bytes(local_path, data)
                    downloaded_paths.append(local_path)
                else:
                    logger.warning(f"Failed to download asset: {asset.url_path}")
            except Exception as e:  # noqa: BLE001
                logger.error(f"Unexpected error downloading {asset.url_path}: {e}")

        return downloaded_paths
