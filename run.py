"""Ponto de entrada: `python run.py --url …` (Clean Architecture em `src/recon/`)."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def main() -> None:
    """Delega para o CLI após garantir `src/` no path."""
    from recon.presentation.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
