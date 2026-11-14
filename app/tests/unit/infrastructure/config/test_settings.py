"""Testes unitarios para Settings."""

from pathlib import Path

import pytest

from infrastructure.config.settings import Settings


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_from_env_defaults(monkeypatch, tmp_path):
    """Valores padrao sao aplicados quando variaveis de ambiente estao ausentes."""
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
    """Valores customizados de ambiente sao carregados."""
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
    """Timeout invalido retorna ao valor padrao 30."""
    monkeypatch.setenv("RECON_DISABLE_DOTENV", "1")
    monkeypatch.setenv("RECON_HTTP_TIMEOUT_SECONDS", "abc")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 30


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_loads_dotenv_file(monkeypatch, tmp_path: Path):
    """Arquivo .env e carregado quando nao esta desabilitado."""
    monkeypatch.delenv("RECON_DISABLE_DOTENV", raising=False)
    monkeypatch.delenv("RECON_HTTP_TIMEOUT_SECONDS", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("RECON_HTTP_TIMEOUT_SECONDS=42\n", encoding="utf-8")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 42


@pytest.mark.unit
@pytest.mark.infrastructure
def test_settings_missing_dotenv_file(monkeypatch, tmp_path: Path):
    """Ausencia de .env e ignorada quando o carregamento de dotenv esta habilitado."""
    monkeypatch.delenv("RECON_DISABLE_DOTENV", raising=False)
    monkeypatch.setenv("RECON_HTTP_TIMEOUT_SECONDS", "11")

    settings = Settings.from_env(tmp_path)
    assert settings.http_timeout_seconds == 11
