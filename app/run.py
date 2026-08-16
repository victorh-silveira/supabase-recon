"""Ponto de entrada da aplicacao."""

import os

from presentation.cli.bootstrap import main
from recon_paths import REPO_ROOT


if __name__ == "__main__":
    os.chdir(REPO_ROOT)
    main(REPO_ROOT)
