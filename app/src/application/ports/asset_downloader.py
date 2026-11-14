"""Contrato de download de assets."""

from pathlib import Path
from typing import Protocol

from domain.entities.asset import Asset


class AssetDownloaderPort(Protocol):
    """Porta para download de assets da aplicacao."""

    def download_all(self, base_url: str, assets: list[Asset], project_dir: Path) -> list[Path]:
        """Baixa os assets a partir de uma URL base para o diretorio do projeto."""
        ...
