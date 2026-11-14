"""Adaptador de repositorio para gerenciar armazenamento fisico em disco."""

from __future__ import annotations

import logging
from pathlib import Path

from infrastructure.logging.events import log_event


logger = logging.getLogger(__name__)


class FileRepository:
    """Gerencia criacao de diretorios e persistencia de arquivos."""

    def __init__(self, base_output_path: str = "output") -> None:
        """Inicializa com um diretorio base (padrao 'output')."""
        self.base_path = Path(base_output_path)

    def get_project_dir(self, domain: str) -> Path:
        """Obtem o diretorio especifico para o dominio do projeto."""
        safe_domain = domain.replace(":", "_").replace("/", "_")
        project_dir = self.base_path / safe_domain
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def write_text(self, file_path: Path, content: str) -> None:
        """Grava conteudo textual em um arquivo."""
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
        """Grava conteudo binario em um arquivo."""
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
        """Localiza o maior arquivo .js dentro de um diretorio (heuristica do bundle principal)."""
        js_files = list(directory.rglob("*.js"))
        if not js_files:
            return None
        return max(js_files, key=lambda p: p.stat().st_size if p.exists() else 0)
