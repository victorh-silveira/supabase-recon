"""Unit tests for Asset model."""

import pytest

from app.domain.models.asset import Asset


@pytest.mark.unit
@pytest.mark.domain
def test_asset_properties():
    """Test Asset helper properties."""
    asset = Asset(url_path="assets/index-ABC.js")
    assert asset.is_js is True
    assert asset.filename == "index-ABC.js"

    asset_css = Asset(url_path="assets/style.css")
    assert asset_css.is_js is False
    assert asset_css.filename == "style.css"
