"""Validation logic for Supabase configuration."""

from domain.entities.supabase_config import SupabaseConfig
from domain.exceptions import ValidationError


class ConfigValidator:
    """Validator for domain entities."""

    @staticmethod
    def validate_supabase_config(config: SupabaseConfig) -> None:
        """Validate the Supabase configuration.

        Args:
            config: The configuration to validate.

        Raises:
            ValidationError: If the configuration is invalid.
        """
        if config.url == "{SUPABASE_URL}":
            raise ValidationError("Supabase URL was not discovered.")

        if config.anon_key == "{ANON_KEY}":
            raise ValidationError("Supabase anonKey was not discovered.")

        if not config.url.startswith("http"):
            raise ValidationError(f"Invalid Supabase URL format: {config.url}")
