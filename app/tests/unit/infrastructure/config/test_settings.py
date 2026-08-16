"""Unit tests for Settings."""

from pathlib import Path

import pytest

from infrastructure.config.settings import Settings


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_from_env_defaults(monkeypatch, tmp_path):
    """Defaults apply when env vars are absent."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.delenv("RECON_HTTP_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("RECON_OUTPUT_BASE_PATH", raising=False)
    monkeypatch.delenv("RECON_LOG_LEVEL", raising=False)

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 30
    assert settings.output_base_path == "output"
    assert settings.log_level == "INFO"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_from_env_custom(monkeypatch, tmp_path):
    """Custom env values are loaded."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setenv("RECON_HTTP_TIMEOUT_SECONDS", "15")
    monkeypatch.setenv("RECON_OUTPUT_BASE_PATH", "out-custom")
    monkeypatch.setenv("RECON_LOG_LEVEL", "debug")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 15
    assert settings.output_base_path == "out-custom"
    assert settings.log_level == "DEBUG"


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_invalid_timeout(monkeypatch, tmp_path):
    """Invalid timeout falls back to 30."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setenv("RECON_HTTP_TIMEOUT_SECONDS", "abc")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 30


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_loads_dotenv_file(monkeypatch, tmp_path: Path):
    """Dotenv file is loaded when not disabled."""
    monkeypatch.delenv("RECON_DISABLE_DOTENV", raising=False)
    monkeypatch.delenv("RECON_HTTP_TIMEOUT_SECONDS", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("RECON_HTTP_TIMEOUT_SECONDS=42\n", encoding="utf-8")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 42


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_missing_dotenv_file(monkeypatch, tmp_path: Path):
    """Missing .env is ignored when dotenv loading is enabled."""
    monkeypatch.delenv("RECON_DISABLE_DOTENV", raising=False)
    monkeypatch.setenv("RECON_HTTP_TIMEOUT_SECONDS", "11")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 11
