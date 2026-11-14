"""Testes unitarios para ConfigValidator."""

import pytest

from domain.entities.supabase_config import SupabaseConfig
from domain.exceptions import ValidationError
from domain.validation.config_validator import ConfigValidator


@pytest.mark.unit
@pytest.mark.domain
def test_validation_success():
    """Testa validacao bem-sucedida."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="eyJ...")
    ConfigValidator.validate_supabase_config(config)


@pytest.mark.unit
@pytest.mark.domain
def test_validation_failure_url():
    """Testa falha de validacao para URL placeholder."""
    config = SupabaseConfig(url="{SUPABASE_URL}", anon_key="eyJ...")
    with pytest.raises(ValidationError, match="Supabase URL was not discovered"):
        ConfigValidator.validate_supabase_config(config)


@pytest.mark.unit
@pytest.mark.domain
def test_validation_failure_key():
    """Testa falha de validacao para chave placeholder."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="{ANON_KEY}")
    with pytest.raises(ValidationError, match="Supabase anonKey was not discovered"):
        ConfigValidator.validate_supabase_config(config)


@pytest.mark.unit
@pytest.mark.domain
def test_validation_failure_format():
    """Testa falha de validacao para formato de URL invalido."""
    config = SupabaseConfig(url="invalid-url", anon_key="eyJ...")
    with pytest.raises(ValidationError, match="Invalid Supabase URL format"):
        ConfigValidator.validate_supabase_config(config)
