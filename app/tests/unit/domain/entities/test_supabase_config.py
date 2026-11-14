"""Testes unitarios para a entidade SupabaseConfig."""

import pytest

from domain.entities.supabase_config import SupabaseConfig


@pytest.mark.unit
@pytest.mark.domain
def test_supabase_config_valid():
    """Testa que uma configuracao completa e valida."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="eyJ...")
    assert config.is_valid is True


@pytest.mark.unit
@pytest.mark.domain
def test_supabase_config_invalid_placeholder():
    """Testa que placeholders tornam a configuracao invalida."""
    config = SupabaseConfig(url="{SUPABASE_URL}", anon_key="{ANON_KEY}")
    assert config.is_valid is False


@pytest.mark.unit
@pytest.mark.domain
def test_supabase_config_empty():
    """Testa que strings vazias tornam a configuracao invalida."""
    config = SupabaseConfig(url="", anon_key="")
    assert config.is_valid is False
