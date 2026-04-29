"""Unit tests for SupabaseConfig model."""

import pytest

from app.domain.models.supabase_config import SupabaseConfig


@pytest.mark.unit
@pytest.mark.domain
def test_supabase_config_valid():
    """Test that a complete config is valid."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="eyJ...")
    assert config.is_valid is True


@pytest.mark.unit
@pytest.mark.domain
def test_supabase_config_invalid_placeholder():
    """Test that placeholders make the config invalid."""
    config = SupabaseConfig(url="{SUPABASE_URL}", anon_key="{ANON_KEY}")
    assert config.is_valid is False


@pytest.mark.unit
@pytest.mark.domain
def test_supabase_config_empty():
    """Test that empty strings make the config invalid."""
    config = SupabaseConfig(url="", anon_key="")
    assert config.is_valid is False
