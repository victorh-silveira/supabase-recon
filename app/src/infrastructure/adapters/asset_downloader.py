"""Adaptador para orquestrar downloads de assets."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.file_repository import FileRepositoryPort
from application.ports.http_client import HttpClientPort
from domain.entities.asset import Asset
from infrastructure.logging.events import log_event


logger = logging.getLogger(__name__)


class AssetDownloader:
    """Orquestra o download de uma lista de assets para o repositorio local."""

    def __init__(self, http_client: HttpClientPort, file_repository: FileRepositoryPort) -> None:
        """Inicializa com as dependencias de rede e persistencia."""
        self.http_client = http_client
        self.file_repository = file_repository

    def download_all(self, base_url: str, assets: list[Asset], project_dir: Path) -> list[Path]:
        """Baixa uma lista de assets a partir de uma URL base para o diretorio do projeto."""
        downloaded_paths: list[Path] = []

        log_event(
            logger,
            logging.INFO,
            "recon.asset.download.started",
            count=len(assets),
            path=str(project_dir),
        )

        for asset in assets:
            full_url = f"{base_url.rstrip('/')}/{asset.url_path.lstrip('/')}"
            local_path = project_dir.joinpath(*asset.url_path.lstrip("/").split("/"))

            try:
                data = self.http_client.get_bytes(full_url)
                if data is not None:
                    self.file_repository.write_bytes(local_path, data)
                    downloaded_paths.append(local_path)
                else:
                    log_event(
                        logger,
                        logging.WARNING,
                        "recon.asset.download.failed",
                        url=full_url,
                        path=asset.url_path,
                    )
            except Exception as e:
                log_event(
                    logger,
                    logging.ERROR,
                    "recon.asset.download.failed",
                    url=full_url,
                    path=asset.url_path,
                    error=str(e),
                    exc_info=True,
                )

        log_event(
            logger,
            logging.DEBUG,
            "recon.asset.download.finished",
            downloaded=len(downloaded_paths),
            total=len(assets),
        )
        return downloaded_paths
