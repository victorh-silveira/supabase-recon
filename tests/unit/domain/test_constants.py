"""Constantes de domínio."""

from __future__ import annotations

from recon.domain.constants import ACCESSIBLE_HTTP_STATUSES, BANNER


def test_banner_non_empty() -> None:
    """Banner ASCII definido para o CLI."""
    assert len(BANNER.strip()) > 10


def test_accessible_statuses_contains_ok_and_authish() -> None:
    """Conjunto de HTTP codes considerados úteis para recon."""
    assert 200 in ACCESSIBLE_HTTP_STATUSES
    assert 422 in ACCESSIBLE_HTTP_STATUSES
