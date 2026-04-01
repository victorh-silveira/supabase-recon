"""Constantes de domínio."""

from __future__ import annotations

from recon.domain.constants import ACCESSIBLE_HTTP_STATUSES, PATH_PARAM_PLACEHOLDERS


def test_path_param_placeholders_non_empty() -> None:
    """Placeholders para sondagem de paths REST/RPC."""
    assert "id" in PATH_PARAM_PLACEHOLDERS
    assert PATH_PARAM_PLACEHOLDERS["id"]


def test_accessible_statuses_contains_ok_and_authish() -> None:
    """Conjunto de HTTP codes considerados úteis para recon."""
    assert 200 in ACCESSIBLE_HTTP_STATUSES
    assert 422 in ACCESSIBLE_HTTP_STATUSES
