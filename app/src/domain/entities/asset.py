"""Modelos de asset para arquivos descobertos da aplicacao."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Asset:
    """Representa um asset estatico (JS, CSS, etc.) a ser baixado ou analisado."""

    url_path: str
    local_path: Path | None = None
    size_bytes: int = 0

    @property
    def is_js(self) -> bool:
        """Verifica se o asset e um arquivo JavaScript."""
        return self.url_path.endswith(".js")

    @property
    def filename(self) -> str:
        """Retorna o nome do arquivo a partir do caminho da URL."""
        return Path(self.url_path).name
