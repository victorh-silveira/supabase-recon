"""Entrypoint shim for Chupabase Analyzer."""

import sys
from pathlib import Path

# Add src to sys.path to allow imports from app
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from main import bootstrap

if __name__ == "__main__":
    bootstrap()
