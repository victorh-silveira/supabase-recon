"""Unit tests for AssetDownloader adapter."""

from pathlib import Path

import pytest

from domain.entities.asset import Asset
from infrastructure.adapters.asset_downloader import AssetDownloader


@pytest.fixture
def downloader():
    """Return an AssetDownloader with fake dependencies."""

    class FakeClient:
        def get_bytes(self, url):
            return b"content"

        def get_text(self, url):
            return None

        def request(self, method, url, headers=None, json_data=None):
            return 200, "OK", ""

    class FakeRepo:
        def write_bytes(self, p, c):
            return None

        def write_text(self, p, c):
            return None

        def get_project_dir(self, domain):
            return Path("out")

        def find_largest_js(self, directory):
            return None

    return AssetDownloader(http_client=FakeClient(), file_repository=FakeRepo())


@pytest.mark.unit
@pytest.mark.infrastructure
def test_download_asset_error(downloader, monkeypatch):
    """Test handling of download errors."""

    def mock_get(*args, **kwargs):
        raise Exception("Fatal error")

    monkeypatch.setattr(downloader.http_client, "get_bytes", mock_get)

    asset = Asset(url_path="fail.js")
    downloader.download_all("https://example.com", [asset], Path("output"))


@pytest.mark.unit
@pytest.mark.infrastructure
def test_download_all(downloader):
    """Test downloading multiple assets."""
    assets = [Asset(url_path="a.js"), Asset(url_path="b.css")]
    downloader.download_all("https://example.com", assets, Path("output"))


@pytest.mark.unit
@pytest.mark.infrastructure
def test_download_all_failure_branch(downloader, monkeypatch):
    """Test the branch where data is None."""
    monkeypatch.setattr(downloader.http_client, "get_bytes", lambda u: None)
    assets = [Asset(url_path="fail.js")]
    paths = downloader.download_all("https://e.com", assets, Path("o"))
    assert len(paths) == 0
