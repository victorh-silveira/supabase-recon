"""Unit tests for AssetDownloader."""

import pytest
from pathlib import Path
from app.domain.models.asset import Asset
from app.infrastructure.loaders.asset_downloader import AssetDownloader


@pytest.fixture
def downloader():
    """Return an AssetDownloader with mocked dependencies."""
    class MockClient:
        def get_bytes(self, url): return b"content"
    class MockRepo:
        def write_bytes(self, p, c): pass
    return AssetDownloader(http_client=MockClient(), file_repository=MockRepo())


@pytest.mark.unit
@pytest.mark.infrastructure
def test_download_asset_error(downloader, monkeypatch):
    """Test handling of download errors."""
    def mock_get(*args, **kwargs):
        raise Exception("Fatal error")
    monkeypatch.setattr(downloader.http_client, "get_bytes", mock_get)
    
    asset = Asset(url_path="fail.js")
    downloader.download_all("https://example.com", [asset], Path("output"))
    # Should skip and log error, not raise


@pytest.mark.unit
@pytest.mark.infrastructure
def test_download_all(downloader):
    """Test downloading multiple assets."""
    assets = [Asset(url_path="a.js"), Asset(url_path="b.css")]
    downloader.download_all("https://example.com", assets, Path("output"))
    # Should work without error


@pytest.mark.unit
@pytest.mark.infrastructure
def test_download_all_failure_branch(downloader, monkeypatch):
    """Test the branch where data is None."""
    monkeypatch.setattr(downloader.http_client, "get_bytes", lambda u: None)
    assets = [Asset(url_path="fail.js")]
    paths = downloader.download_all("https://e.com", assets, Path("o"))
    assert len(paths) == 0
