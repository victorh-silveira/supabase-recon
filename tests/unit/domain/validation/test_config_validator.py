"""Unit tests for ConfigValidator."""

import pytest
from app.domain.exceptions import ValidationError
from app.domain.models.supabase_config import SupabaseConfig
from app.domain.validation.config_validator import ConfigValidator


@pytest.mark.unit
@pytest.mark.domain
def test_validation_success():
    """Test successful validation."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="eyJ...")
    ConfigValidator.validate_supabase_config(config)  # Should not raise


@pytest.mark.unit
@pytest.mark.domain
def test_validation_failure_url():
    """Test validation failure for placeholder URL."""
    config = SupabaseConfig(url="{SUPABASE_URL}", anon_key="eyJ...")
    with pytest.raises(ValidationError, match="Supabase URL was not discovered"):
        ConfigValidator.validate_supabase_config(config)


@pytest.mark.unit
@pytest.mark.domain
def test_validation_failure_key():
    """Test validation failure for placeholder key."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="{ANON_KEY}")
    with pytest.raises(ValidationError, match="Supabase anonKey was not discovered"):
        ConfigValidator.validate_supabase_config(config)


@pytest.mark.unit
@pytest.mark.domain
def test_validation_failure_format():
    """Test validation failure for invalid URL format."""
    config = SupabaseConfig(url="invalid-url", anon_key="eyJ...")
    with pytest.raises(ValidationError, match="Invalid Supabase URL format"):
        ConfigValidator.validate_supabase_config(config)
