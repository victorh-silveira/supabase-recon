"""Validation logic for Supabase configuration."""

import logging

from app.domain.exceptions import ValidationError
from app.domain.models.supabase_config import SupabaseConfig


logger = logging.getLogger(__name__)


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

        logger.info("Supabase configuration validated successfully.")
